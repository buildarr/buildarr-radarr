# Copyright (C) 2023 Callum Dickinson
#
# Buildarr is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Buildarr is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Buildarr.
# If not, see <https://www.gnu.org/licenses/>.


"""
Radarr import list configuration.
"""


from __future__ import annotations

from logging import getLogger
from typing import Any, Dict, Iterable, List, Literal, Mapping, Optional, Set, Union, cast

from buildarr.config import RemoteMapEntry
from buildarr.state import state
from buildarr.types import InstanceName, NonEmptyStr
from pydantic import AnyHttpUrl, Field, PositiveInt, validator
from typing_extensions import Self

from ....api import api_get
from ....secrets import RadarrSecrets
from ....types import ArrApiKey
from .base import ImportList

logger = getLogger(__name__)


class RadarrImportList(ImportList):
    """
    Import items from another Radarr instance.

    ```yaml
    ...
      import_lists:
        definitions:
          Radarr:
            type: "radarr"
            # Global import list options.
            root_folder: "/path/to/videos"
            quality_profile: "HD/SD"
            # Radarr import list-specific options.
            full_url: "http://radarr:7878"
            api_key: "1a2b3c4d5e1a2b3c4d5e1a2b3c4d5e1a"
            source_quality_profiles:
              - 11
              ...
            source_tags:
              - 33
              ...
    ```

    This import list supports instance references to another Buildarr-defined Radarr instance
    using `instance_name`.

    In this mode, you can specify `instance_name` in place of `api_key`,
    and use actual names for the source quality profiles and tags,
    instead of IDs which are subject to change.

    Here is an example of one Radarr instance (`radarr-4k`) referencing
    another instance (`radarr-hd`), using it as an import list.

    ```yaml
    radarr:
      instances:
        radarr-hd:
          hostname: "localhost"
          port: 7878
        radarr-4k:
          hostname: "localhost"
          port: 7879
          settings:
            import_lists:
              definitions:
                Radarr (HD):
                  type: "radarr"
                  # Global import list options.
                  root_folder: "/path/to/videos"
                  quality_profile: "4K"
                  # Radarr import list-specific options.
                  full_url: "http://radarr:7878"
                  instance_name: "radarr-hd"
                  source_quality_profiles:
                    - "HD/SD"
                  source_tags:
                    - "shows"
    ```

    An important thing to keep in mind is that unless Buildarr is on the same network
    as the rest of the *Arr stack, the hostnames and ports may differ to what the
    Radarr instances will use to communicate with each other. `full_url` should be
    set to what the Radarr instance itself will use to link to the target instance.
    """

    type: Literal["radarr"] = "radarr"
    """
    Type value associated with this kind of import list.
    """

    instance_name: Optional[InstanceName] = Field(None, plugin="radarr")
    """
    The name of the Radarr instance within Buildarr, if linking this Radarr instance
    with another Buildarr-defined Radarr instance.

    *New in version 0.3.0.*
    """

    full_url: AnyHttpUrl
    """
    The URL that this Radarr instance will use to connect to the source Radarr instance.
    """

    api_key: Optional[ArrApiKey] = None
    """
    API key used to access the source Radarr instance.

    If a Radarr instance managed by Buildarr is not referenced using `instance_name`,
    this attribute is required.
    """

    source_quality_profiles: Set[Union[PositiveInt, NonEmptyStr]] = Field(
        set(),
        alias="source_quality_profile_ids",
    )
    """
    List of IDs (or names) of the quality profiles on the source instance to import from.

    Quality profile names can only be used if `instance_name` is used to
    link to a Buildarr-defined Radarr instance.
    If linking to a Radarr instance outside Buildarr, IDs must be used.

    *Changed in version 0.3.0*: Renamed from `source_quality_profile_ids`
    (which is still valid as an alias), and added support for quality profile names.
    """

    source_tags: Set[Union[PositiveInt, NonEmptyStr]] = Field(set(), alias="source_tag_ids")
    """
    List of IDs (or names) of the tags on the source instance to import from.

    Tag names can only be used if `instance_name` is used to
    link to a Buildarr-defined Radarr instance.
    If linking to a Radarr instance outside Buildarr, IDs must be used.

    *Changed in version 0.3.0*: Renamed from `source_tag_ids`
    (which is still valid as an alias), and added support for tag names.
    """

    _implementation: str = "RadarrImport"
    _remote_map: List[RemoteMapEntry] = []

    @classmethod
    def _get_base_remote_map(
        cls,
        quality_profile_ids: Mapping[str, int],
        tag_ids: Mapping[str, int],
    ) -> List[RemoteMapEntry]:
        return [
            *super()._get_base_remote_map(
                quality_profile_ids=quality_profile_ids,
                tag_ids=tag_ids,
            ),
            ("full_url", "baseUrl", {"is_field": True}),
            ("api_key", "apiKey", {"is_field": True}),
            (
                "source_quality_profiles",
                "profileIds",
                {
                    "is_field": True,
                    "root_encoder": lambda vs: cls._encode_source_resources(
                        instance_name=vs.instance_name,
                        resources=vs.source_quality_profiles,
                        resource_type="qualityprofile",
                    ),
                },
            ),
            (
                "source_tags",
                "tagIds",
                {
                    "is_field": True,
                    "root_encoder": lambda vs: cls._encode_source_resources(
                        instance_name=vs.instance_name,
                        resources=vs.source_tags,
                        resource_type="tag",
                        name_key="label",
                    ),
                },
            ),
        ]

    @classmethod
    def _get_secrets(cls, instance_name: str) -> RadarrSecrets:
        """
        Fetch the secrets metadata for the given Radarr instance from the Buildarr state.

        Args:
            instance_name (str): Name of Radarr instance to get the secrets for.

        Returns:
            Radarr instance secrets metadata
        """
        return cast(RadarrSecrets, state.instance_secrets["radarr"][instance_name])

    @classmethod
    def _get_resources(cls, instance_name: str, resource_type: str) -> List[Dict[str, Any]]:
        """
        Make an API request to Radarr to get the list of resources of the requested type.

        Args:
            instance_name (str): Name of Radarr instance to get the resources from.
            profile_type (str): Name of the resource to get in the Radarr API.

        Returns:
            List of resource API objects
        """
        return api_get(cls._get_secrets(instance_name), f"/api/v3/{resource_type}")

    @validator("api_key", always=True)
    def validate_api_key(
        cls,
        value: Optional[ArrApiKey],
        values: Mapping[str, Any],
    ) -> Optional[ArrApiKey]:
        """
        Validate the `api_key` attribute after parsing.

        Args:
            value (Optional[str]): `api_key` value.
            values (Mapping[str, Any]): Currently parsed attributes. `instance_name` is checked.

        Raises:
            ValueError: If `api_key` is undefined when `instance_name` is also undefined.

        Returns:
            Validated `api_key` value
        """
        if not values.get("instance_name", None) and not value:
            raise ValueError("required if 'instance_name' is undefined")
        return value

    @validator("source_quality_profiles", "source_tags", each_item=True)
    def validate_source_resource_ids(
        cls,
        value: Union[int, str],
        values: Dict[str, Any],
    ) -> Union[int, str]:
        """
        Validate that all resource references are IDs (integers) if `instance_name` is undefined.

        Args:
            value (Union[int, str]): Resource reference (ID or name).
            values (Mapping[str, Any]): Currently parsed attributes. `instance_name` is checked.

        Raises:
            ValueError: If the resource reference is a name and `instance_name` is undefined.

        Returns:
            Validated resource reference
        """
        if not values.get("instance_name", None) and not isinstance(value, int):
            raise ValueError(
                "values must be IDs (not names) if 'instance_name' is undefined",
            )
        return value

    @classmethod
    def _encode_source_resources(
        cls,
        instance_name: Optional[str],
        resources: Iterable[Union[str, int]],
        resource_type: str,
        name_key: str = "name",
    ) -> List[int]:
        """
        Encode a collection of resource IDs/names into a list of resource IDs
        from the target Radarr instance.

        Args:
            instance_name (Optional[str]): Target Radarr instance to get resource IDs from.
            resources (Iterable[Union[str, int]]): Resource names/IDs to encode.
            resource_type (str): Type of resource to encode into IDs.
            name_key (str, optional): Key for the name of the resource. Defaults to `name`.

        Returns:
            List of resource IDs for the target Radarr instance
        """
        resource_ids: Set[int] = set()
        if not instance_name:
            for resource in resources:
                if not isinstance(resource, int):
                    raise RuntimeError(
                        f"{resource_type} reference should be of type int here: {resource}",
                    )
                resource_ids.add(resource)
            return sorted(resource_ids)
        source_resource_ids: Optional[Dict[str, int]] = None
        for resource in resources:
            if isinstance(resource, int):
                resource_ids.add(resource)
            else:
                if source_resource_ids is None:
                    source_resource_ids = {
                        p[name_key]: p["id"]
                        for p in cls._get_resources(
                            instance_name,
                            resource_type,
                        )
                    }
                try:
                    resource_ids.add(source_resource_ids[resource])
                except KeyError as err:
                    raise RuntimeError(
                        f"Unable to find ID for {resource_type} '{err.args[0]}'",
                    ) from None
        return sorted(resource_ids)

    def _resolve_from_local(
        self,
        name: str,
        local: Self,
        ignore_nonexistent_ids: bool = False,
    ) -> Self:
        instance_name = local.instance_name
        if not instance_name:
            return self
        api_key = self._get_secrets(instance_name).api_key
        source_quality_profiles = self._resolve_resources(
            name=name,
            instance_name=instance_name,
            source_resources=self.source_quality_profiles,
            resource_type_int="quality_profile",
            resource_type_ext="qualityprofile",
            resource_description="quality profile",
            ignore_nonexistent_ids=ignore_nonexistent_ids,
        )
        source_tags = self._resolve_resources(
            name=name,
            instance_name=instance_name,
            source_resources=self.source_tags,
            resource_type_int="tag",
            resource_type_ext="tag",
            resource_description="tag",
            ignore_nonexistent_ids=ignore_nonexistent_ids,
            name_key="label",
        )
        return self.copy(
            update={
                "instance_name": instance_name,
                "api_key": api_key,
                "source_quality_profiles": source_quality_profiles,
                "source_tags": source_tags,
            },
        )

    def _resolve_resources(
        self,
        name: str,
        instance_name: str,
        source_resources: Iterable[Union[int, str]],
        resource_type_int: str,
        resource_type_ext: str,
        resource_description: str,
        ignore_nonexistent_ids: bool,
        name_key: str = "name",
    ) -> Set[Union[int, str]]:
        """
        Resolve target Radarr instance resource IDs/names into resource names.

        If `ignore_nonexistent_ids` is `True` and a resource ID was not found
        on the Radarr instance, it is returned as-is.
        This will prompt Buildarr to remove the offending ID from Radarr,
        so a warning is output to the logs to notify the user.

        Args:
            name (str): Name associated with this import list.
            instance_name (str): Target Radarr instance name in Buildarr.
            source_resources (Iterable[Union[int, str]]):
            resource_type (str): Type of resource to resolve IDs for names.
            resource_description (str): Description of the resource type for logging.
            ignore_nonexistent_ids (bool): If `True`, remove non-existent IDs from the remote.
            name_key (str, optional): _description_. Defaults to "name".

        Raises:
            ValueError: If a non-existent ID was found and `ignore_nonexistent_ids` is `False`.
            ValueError: If a resource name was not found on the target Radarr instance.

        Returns:
            List of resolved source resource names (and invalid IDs)
        """
        resolved_source_resources: Set[Union[int, str]] = set()
        if not source_resources:
            return resolved_source_resources
        remote_resources = self._get_resources(instance_name, resource_type_ext)
        resource_ids = {r[name_key]: r["id"] for r in remote_resources}
        resource_names = {r["id"]: r[name_key] for r in remote_resources}
        for resource in source_resources:
            if isinstance(resource, int):
                try:
                    resolved_source_resources.add(resource_names[resource])
                except KeyError:
                    if ignore_nonexistent_ids:
                        logger.warning(
                            (
                                "Source %s ID %i referenced by remote Radarr instance "
                                "not found on target instance '%s', removing"
                            ),
                            resource_description,
                            resource,
                            instance_name,
                        )
                        resolved_source_resources.add(resource)
                    else:
                        raise ValueError(
                            f"Source {resource_description} ID {resource} "
                            f"not found on target instance '{instance_name}",
                        ) from None
            elif resource in resource_ids:
                resolved_source_resources.add(resource)
            else:
                available_resources = list(resource_ids.keys())
                _resources_str = (
                    ", ".join(repr(p) for p in available_resources)
                    if available_resources
                    else "(none)"
                )
                error_message = (
                    f"Source {resource_description} '{resource}' "
                    f"not found on target Radarr instance '{instance_name}' "
                    f"in import list '{name}' "
                    f"(available {resource_description}s: {_resources_str})"
                )
                raise ValueError(error_message)
        return resolved_source_resources
