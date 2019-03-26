from sqlalchemy import create_engine #sudo pip show
import pandas as pd #0.24.1

# Seting Database
username = 'root'
password = 'toor'
host = 'localhost'
port = '3306'
database = 'db_log'
table = 'tb_test2'

class sql_con():
    def __init__(self, table):
        self.table = table
        try:
            engine = create_engine('mysql+mysqlconnector://'+username+':'+password+'@'+host+':'+port+'/'+database+'?use_unicode=true')
            self.con = engine.connect()
            self.connected = True
        except:
            # print('Error: Koneksi ke DB gagal!')
            self.connected = False
        self.df = pd.read_sql(self.table, con=con)
    def deduplicate(self, fieldname): #fieldname =['shortcode']
        if (self.connected):
            self.df = self.df.drop_duplicates(subset=fieldname,keep='first')
            self.df.to_sql(name=self.table ,con=con,if_exists='replace')
    def add_data(self, data):
        self.df.append(data)
        self.df.to_sql(name=self.table ,con=con,if_exists='replace')
    def make_csv(self, name):
        self.df.to_csv(name, sep=",", index=False)
        print('Saved as', str(name))