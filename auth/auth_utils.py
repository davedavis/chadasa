import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/sdm.service",
    "https://www.googleapis.com/auth/pubsub",
    "https://www.googleapis.com/auth/cloud-platform",
]


def get_credentials(client_secrets_file):
    if not os.path.exists("credentials.dat"):

        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        credentials = flow.run_local_server()

        with open("credentials.dat", "wb") as credentials_dat:
            pickle.dump(credentials, credentials_dat)

    else:
        with open("credentials.dat", "rb") as credentials_dat:
            credentials = pickle.load(credentials_dat)
            # print(credentials.refresh_token)

            # ToDo: Check for existence of refresh token.
            # If it doesn't exist, delete .dat & trigger the initial flow again

    if credentials.expired:
        credentials.refresh(Request())

    return credentials


def get_service_account_credentials(credentials_file):
    # ToDo: Reimplement this
    service_credentials = service_account.Credentials.from_service_account_file(
        credentials_file
    )
