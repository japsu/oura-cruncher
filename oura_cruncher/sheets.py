import os.path
from functools import cache
from typing import TYPE_CHECKING

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import config

if TYPE_CHECKING:
    from .night import Night

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


@cache
def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_existing_range(
    existing_data: list[str],
    lookup_key: str,
    lookup_field: str = "day",
    # TODO un-hardcode perhaps?
    first_col: str = "A",
    last_col: str = "F",
):
    """
    >>> shieet = [["day", "bar"], ["2022-07-11", "quux"]]
    >>> get_existing_range(shieet, "2022-07-11")
    'A2:C2'
    >>> get_existing_range(shieet, "2022-07-12")
    """

    header_row = existing_data[0]
    col_0 = header_row.index(lookup_field)

    try:
        row_0 = [row[col_0] for row in existing_data].index(lookup_key)
    except ValueError:
        # not found
        return None
    else:
        row_1 = row_0 + 1
        return f"{first_col}{row_1}:{last_col}{row_1}"


def put_nights_data(
    nights: list["Night"],
    spreadsheet_id=config.sheets.sheet_id,
    range=config.sheets.range,
):
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet_values = service.spreadsheets().values()
    result = sheet_values.get(spreadsheetId=spreadsheet_id, range=range).execute()
    existing_data = result["values"]

    update_value_ranges = []
    append_rows = []

    for night in nights:
        existing_range = get_existing_range(existing_data, night.day)
        if existing_range:
            update_value_ranges.append(
                dict(
                    range=existing_range,
                    majorDimension="ROWS",
                    values=[night.sheets_row],
                )
            )
        else:
            append_rows.append(night.sheets_row)

    if update_value_ranges:
        sheet_values.batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=dict(
                value_input_option="USER_ENTERED",
                data=update_value_ranges,
            ),
        ).execute()

    if append_rows:
        sheet_values.append(
            spreadsheetId=spreadsheet_id,
            range=range,
            valueInputOption="USER_ENTERED",
            insertDataOption="OVERWRITE",
            includeValuesInResponse=False,
            body=dict(
                range=range,
                majorDimension="ROWS",
                values=append_rows,
            ),
        ).execute()


def get_nights_data(spreadsheet_id=config.sheets.sheet_id, range=config.sheets.range):
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet_values = service.spreadsheets().values()
    result = sheet_values.get(spreadsheetId=spreadsheet_id, range=range).execute()
    existing_data = result["values"]

    header_row = existing_data[0]
    return [dict(zip(header_row, row)) for row in existing_data[1:]]
