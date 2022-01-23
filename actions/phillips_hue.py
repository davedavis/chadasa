"""Example script for using AIOHue connecting to a V2 Hue bridge."""
import asyncio
from aiohue.discovery import discover_nupnp
from aiohue import HueBridgeV2
from config.settingsfile import get_settings


async def get_bridge():
    discovered_bridges = await discover_nupnp()
    for item in discovered_bridges:
        return item.host


async def get_light_ids(hue_host):
    async with HueBridgeV2(hue_host, get_settings()["phillips_hue_api_user"]) as bridge:
        print("Connected to bridge: ", bridge.config.name)
        print()
        print("Found these lights: ")
        for light in bridge.lights:
            print(
                "Light #: ",
                light.id_v1[8:],
                "\t ID --->>>\t" + light.id + "\t--->>>\t" + light.metadata.name,
            )


async def flash_lights(hue_host):

    async with HueBridgeV2(hue_host, get_settings()["phillips_hue_api_user"]) as bridge:

        print("Connected to bridge: ", bridge.bridge_id)
        print(bridge.config.bridge_device)

        print()
        print("found lights:")
        for item in bridge.lights:
            print(item.metadata.name)

        print()
        print("found devices:")
        for item in bridge.devices:
            print(item.metadata.name)

        # turn on a light
        light = bridge.lights.items[13]
        print("Turning on light", light.name)
        await bridge.lights.turn_on(light.id)
        await asyncio.sleep(1)
        print("Set brightness 100 to light", light.name)
        await bridge.lights.set_brightness(light.id, 100, 2000)
        await asyncio.sleep(2)
        print("Set color to light", light.name)
        await bridge.lights.set_color(light.id, 0.141, 0.123, 2000)
        await asyncio.sleep(1)
        print("Turning off light", light.name)
        # await bridge.lights.turn_off(light.id, 2000)
        # await bridge.lights.set_state(light.id, alert=AlertEffectType.BREATHE)
        await bridge.lights.set_flash(light.id, short=True)

        print()
        print("Subscribing to events...")

        def print_event(event_type, item):
            print()
            print("received event", event_type.value, item)
            print()

        bridge.subscribe(print_event)

        await asyncio.sleep(3)


async def flash_selected_lights(hue_host, lights_to_flash):

    async with HueBridgeV2(hue_host, get_settings()["phillips_hue_api_user"]) as bridge:

        for light in lights_to_flash:
            await bridge.lights.set_flash(light, short=False)

        print()
        print("Subscribing to events...")

        def print_event(event_type, item):
            print()
            print("received event", event_type.value, item)
            print()

        bridge.subscribe(print_event)

        await asyncio.sleep(3)


# try:
#     hue_host = asyncio.run(get_bridge())
#     asyncio.run(main(hue_host))
# except KeyboardInterrupt:
#     pass
