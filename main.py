import json
from googleapiclient.discovery import build
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from auth.auth_utils import get_credentials

DEVICE_ACCESS_CONSOLE_PROJECT_ID = 'd67a6dea-4184-423f-ac66-22793ca538d0'
CLOUD_PROJECT_ID = "chadasa-338300"
PUB_SUB_SUBSCRIPTION_ID = "chadasa-subscription"


def get_messages(credentials_file):
    timeout = 20

    subscriber = pubsub_v1.SubscriberClient(credentials=credentials_file)
    subscription_path = subscriber.subscription_path(CLOUD_PROJECT_ID, PUB_SUB_SUBSCRIPTION_ID)

    def callback(message: pubsub_v1.subscriber.message.Message) -> None:
        print(f"Received {message.data!r}.")

        # Grab the events
        json_response = json.loads(message.data.decode())
        for key, value in json_response['resourceUpdate']['events'].items():
            print(f"{key}: {value}")

        # Get custom attributes if they exist.
        if message.attributes:
            print("Attributes:")
            for key in message.attributes:
                value = message.attributes.get(key)
                print(f"{key}: {value}")
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
            # streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.


def main(authorized_credentials):
    parent = "enterprises/" + DEVICE_ACCESS_CONSOLE_PROJECT_ID
    sdm = build('smartdevicemanagement', 'v1', credentials=authorized_credentials)
    structures = sdm.enterprises().structures().list(parent=parent).execute()
    devices = sdm.enterprises().devices().list(parent=parent).execute()

    print(structures)
    print(devices)


if __name__ == '__main__':
    authorized_credentials = get_credentials('./client_secrets.json')
    main(authorized_credentials)
    get_messages(authorized_credentials)
