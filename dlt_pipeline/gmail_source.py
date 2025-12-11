import os
import pickle
import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.utils import parsedate_to_datetime

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CREDENTIALS_FILE = os.path.join('..', 'credentials', 'oauth_client.json')
TOKEN_FILE = os.path.join('..', 'tokens', 'token.pickle')


def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def extract_more_metadata(msg_detail):
    """Extracts extra structured metadata for analytical charts."""

    headers = {h["name"]: h["value"] for h in msg_detail["payload"]["headers"]}

    raw_date = headers.get("Date")
    dt = parsedate_to_datetime(raw_date) if raw_date else None

    return {
        "Id": msg_detail["id"],
        "From": headers.get("From"),
        "From_Email": headers.get("From").split("<")[-1].replace(">", "") if headers.get("From") else None,
        "Subject": headers.get("Subject"),
        "To": headers.get("To"),
        "Date_Raw": raw_date,
        "Date": dt.isoformat() if dt else None,
        "Date_Day": dt.date().isoformat() if dt else None,
        "Hour": dt.hour if dt else None,
        "Weekday": dt.strftime("%A") if dt else None,
        "Labels": ",".join(msg_detail.get("labelIds", []))
    }


def fetch_emails(max_results=100):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    data = []

    for msg in messages:
        msg_detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=["From", "Subject", "Date", "To"]
        ).execute()

        meta = extract_more_metadata(msg_detail)
        data.append(meta)

    return pd.DataFrame(data)


if __name__ == "__main__":
    df = fetch_emails(30)
    print(df.head())