# Copyright 2022 Dave Davis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from actions.phillips_hue import get_bridge, flash_lights, get_light_ids
from auth.auth_utils import get_credentials
from enums.sdm import Event
from sdm.device_management import get_sdm_hierarchy, monitor_sdm_messages
from rich.console import Console

console = Console()


def main():
    # Get Structures & Devices from SDM API
    authorized_credentials = get_credentials("./client_secrets.json")
    structures, devices = get_sdm_hierarchy(authorized_credentials)

    console.print(
        "[bold red]Nest Devices Detected![/bold red] The following structures "
        "& devices were found on your network:"
    )
    console.print(structures, devices)

    console.print(
        "[bold red]Hue Lights Detected![/bold red] The following structures "
        "& devices were found on your network:"
    )
    try:
        hue_host = asyncio.run(get_bridge())
        asyncio.run(get_light_ids(hue_host))
    except KeyboardInterrupt:
        pass

    # What do you want to respond to?
    # Current options are: BELL_PRESS_DETECTED or PERSON_DETECTED.
    respond_to = Event.BELL_PRESS_DETECTED

    # What lights would you like to flash?
    console.print(
        "[bold purple]Pick out the IDs from the lights on your"
        " network that you want to flash and enter them in"
        " the next method[/bold purple]"
    )

    # Important, replace with the IDs of your own lights.
    lights_to_flash = [
        "161d251f-c9f2-45b8-a9e3-e77486c8b83c",
        "fa462ec8-372b-4afc-a9cc-bf9e17dc8e7b",
    ]

    # Subscribe to SDM events
    monitor_sdm_messages(authorized_credentials, respond_to, lights_to_flash)


if __name__ == "__main__":
    main()
