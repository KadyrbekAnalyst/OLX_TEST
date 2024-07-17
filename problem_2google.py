import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

# Список API
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Cred keys
credentials = Credentials.from_service_account_file('even-ruler-403804-bd6b3d83fc9c.json', scopes=scopes) # the json cred for connect to google service - even-ruler-403804-bd6b3d83fc9c.json

# Авторизация
gc = gspread.authorize(credentials)

# Google key
gs = gc.open_by_key('1smY4dCVOOVxkB0BmdSFoCCiiiEjrYi1cCyiitX36TmU')

# Select a worksheet by name
worksheet1 = gs.worksheet('Test task')

# Очищение данных
worksheet1.clear()

# Загрузка df
df = pd.read_excel('dataframe_overlap.xlsx')

# Upload the DataFrame to Google Sheets
set_with_dataframe(worksheet1, df)

print("DataFrame successfully uploaded to Google Sheets.")



    
    