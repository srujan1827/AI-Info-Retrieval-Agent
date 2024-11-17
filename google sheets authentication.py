def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(
        "C:/Users/Srujan/Downloads/plenary-ability-441810-v5-6190ccd6faa1.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return credentials

def load_google_sheet(sheet_url, credentials):
    # Extract the Google Sheets ID from the URL
    sheet_id = sheet_url.split("/")[5]
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range='Sheet1').execute()
    values = result.get('values', [])
    
    # Convert the data into a DataFrame
    if values:
        df = pd.DataFrame(values[1:], columns=values[0])  # Assumes the first row is the header
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no data is found
