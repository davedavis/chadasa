import asyncio

from actions.phillips_hue import get_bridge, flash_selected_lights
from config.settingsfile import get_settings
import json
from googleapiclient.discovery import build
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

from enums.sdm import Event
from rich.console import Console

console = Console()

DEVICE_ACCESS_CONSOLE_PROJECT_ID = get_settings()["device_access_console_project_id"]
CLOUD_PROJECT_ID = get_settings()["cloud_project_id"]
PUB_SUB_SUBSCRIPTION_ID = get_settings()["pub_sub_subscription_id"]


def get_sdm_hierarchy(creds):
    parent = "enterprises/" + DEVICE_ACCESS_CONSOLE_PROJECT_ID
    sdm = build("smartdevicemanagement", "v1", credentials=creds)
    structures = sdm.enterprises().structures().list(parent=parent).execute()
    devices = sdm.enterprises().devices().list(parent=parent).execute()
    structure_list = []
    device_list = []

    # Return the friendly names in a list. If you want the entire resource,
    # return 'structures, devices'.
    for structure in structures["structures"]:
        structure_list.append(
            structure["traits"]["sdm.structures.traits.Info"]["customName"]
        )

    for device in devices["devices"]:
        device_list.append(device["traits"]["sdm.devices.traits.Info"]["customName"])

    return structure_list, device_list


def monitor_sdm_messages(credentials_file, respond_to, lights_to_flash):
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials_file)
    subscription_path = subscriber.subscription_path(
        CLOUD_PROJECT_ID, PUB_SUB_SUBSCRIPTION_ID
    )

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        # Print the entire response.
        print(f"Received {message.data!r}.")

        # Grab the events
        json_response = json.loads(message.data.decode())
        for key, value in json_response["resourceUpdate"]["events"].items():
            print(f"{key}: {value}")

            # if 'sdm.devices.events.DoorbellChime.Chime' in key:
            if (
                respond_to == Event.BELL_PRESS_DETECTED
                and "sdm.devices.events.DoorbellChime.Chime" in key
            ):
                print("Doorbell detected!")
                hue_host = asyncio.run(get_bridge())
                asyncio.run(flash_selected_lights(hue_host, lights_to_flash))

        # Get custom attributes if they exist.
        if message.attributes:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print(f"{key}: {value}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first. If you want to run
            # this indefinitely, remove the timeout argument completely and
            # pass no arguments at all.
            # streaming_pull_future.result(timeout=timeout)
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until shutdown is complete.
        except KeyboardInterrupt:
            console.print("[bold green]Application terminated. No longer "
                          "monitoring your nest devices. [/bold green] ")
