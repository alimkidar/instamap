from sqlalchemy import create_engine #sudo pip show
import pandas as pd #0.24.1

# Seting Database
username = 'root'
password = 'toor'
host = 'localhost'
port = '3306'
database = 'db_log'
table = 'tb_test2'

try:
    engine = create_engine('mysql+mysqlconnector://'+username+':'+password+'@'+host+':'+port+'/'+database+'?use_unicode=true')
    con = engine.connect()
    connected = True
except:
    print('Error: Koneksi ke DB gagal!')
    connected = False
if (connected):
    df = pd.read_sql(table, con=con)
    df = df.drop_duplicates(subset=['shortcode'],keep='first')
    df.to_sql(name=table ,con=con,if_exists='replace')
    
    