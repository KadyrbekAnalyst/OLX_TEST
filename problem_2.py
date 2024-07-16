import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

# Create a cursor object
cur = conn.cursor()

if cur:
    print("Подключение к базе прошло успешно !!!")
    

# print("Выгружаем таблицу !!!")
    
cur.execute(
    '''
    SELECT
    user_id,
    category_id,
    category_name,
    COUNT(*) AS ads,
    RANK() OVER (PARTITION BY user_id ORDER BY COUNT(*)  DESC) AS category_rank
    FROM ads
    GROUP BY user_id, category_id , category_name;
    '''
)

querry = cur.fetchall()


df = pd.DataFrame(querry, columns=['user_id', 'category_id', 'category_name' , 'ads' , 'rank'])



cur.close()
conn.close()


# print(df.head())


pivot_table = df.pivot_table(index='user_id', columns='category_name', values='ads', aggfunc='sum', fill_value=0)


category_overlap = pd.DataFrame(index=pivot_table.columns, columns=pivot_table.columns)


for category_a in pivot_table.columns:
    for category_b in pivot_table.columns:
        category_overlap.loc[category_a, category_b] = ((pivot_table[category_a] > 0) & (pivot_table[category_b] > 0)).sum()

# print(category_overlap)


if __name__ == "__main__":
    print("Выгружаем Dataframe")
    category_overlap.to_excel('dataframe_overlap.xlsx')
    