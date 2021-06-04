
import sqlite3
import pandas as pd

def get_data(email):
  conn = sqlite3.connect('../users.db')

  # if even once it is marked as wasted, we keep it as so. 
  query = '''select url, max(wasted) as wasted
         from Events where email = '{}'
         group by url'''.format(email)

  df = pd.read_sql_query(query, conn)
  conn.close()
  return df