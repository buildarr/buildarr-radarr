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
Radarr plugin CLI commands.
"""


from __future__ import annotations

import functools

from getpass import getpass
from typing import cast
from urllib.parse import urlparse

import click

from buildarr.types import NonEmptyStr, Port

from .config import RadarrInstanceConfig
from .manager import RadarrManager
from .secrets import RadarrSecrets
from .types import ArrApiKey, RadarrProtocol

HOSTNAME_PORT_TUPLE_LENGTH = 2


@click.group(help="Radarr instance ad-hoc commands.")
def radarr():
    """
    Radarr instance ad-hoc commands.
    """

    pass


@radarr.command(
    help=(
        "Dump configuration from a remote Radarr instance.\n\n"
        "The configuration is dumped to standard output in Buildarr-compatible YAML format."
    ),
)
@click.argument("url", type=click.STRING)
@click.option(
    "-k",
    "--api-key",
    "api_key",
    metavar="API-KEY",
    default=functools.partial(getpass, "Radarr instance API key: "),
    help="API key of the Radarr instance. The user will be prompted if undefined.",
)
def dump_config(url: str, api_key: str) -> int:
    """
    Dump configuration from a remote Radarr instance.
    The configuration is dumped to standard output in Buildarr-compatible YAML format.
    """

    url_obj = urlparse(url)
    protocol = url_obj.scheme
    hostname_port = url_obj.netloc.split(":", 1)
    hostname = hostname_port[0]
    port = (
        int(hostname_port[1])
        if len(hostname_port) == HOSTNAME_PORT_TUPLE_LENGTH
        else (443 if protocol == "https" else 80)
    )

    click.echo(
        RadarrManager()
        .from_remote(
            instance_config=RadarrInstanceConfig(
                hostname=cast(NonEmptyStr, hostname),
                port=cast(Port, port),
                protocol=cast(RadarrProtocol, protocol),
            ),
            secrets=RadarrSecrets(
                hostname=cast(NonEmptyStr, hostname),
                port=cast(Port, port),
                protocol=cast(RadarrProtocol, protocol),
                api_key=cast(ArrApiKey, api_key),
            ),
        )
        .yaml(),
    )

    return 0
