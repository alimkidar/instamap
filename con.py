from sqlalchemy import create_engine #sudo pip show
import pandas as pd #0.24.1

try:
    engine = create_engine('mysql+mysqlconnector://'+username+':'+password+'@'+host+':'+port+'/'+database+'?use_unicode=true')
    con = engine.connect()
    df.to_sql(name=table ,con=con,if_exists='append')
except:
    print('Error: Koneksi ke DB gagal!')
    