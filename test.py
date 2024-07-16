import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

# Define the scopes
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Load the credentials from the JSON file
credentials = Credentials.from_service_account_file('even-ruler-403804-bd6b3d83fc9c.json', scopes=scopes)

# Authorize the client
gc = gspread.authorize(credentials)

# Open a Google Sheet by key
gs = gc.open_by_key('1smY4dCVOOVxkB0BmdSFoCCiiiEjrYi1cCyiitX36TmU')

# Select a worksheet by name
worksheet1 = gs.worksheet('Test task')

# DataFrame to upload
data = {
    'Category A': [1, 2, 3],
    'Category B': [4, 5, 6],
    'Category C': [7, 8, 9]
}
df = pd.DataFrame(data)


# Upload the DataFrame to Google Sheets
set_with_dataframe(worksheet1, df)

print("DataFrame successfully uploaded to Google Sheets.")
worksheet1.clear()
