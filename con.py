from sqlalchemy import create_engine #sudo pip show
import pandas as pd #0.24.1

# Seting Database
username = 'root'
password = 'alimkidar'
host = 'localhost'
port = '3306'
database = 'db_log'

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
        if (self.connected):
            try:
                self.df = pd.read_sql(self.table, con=self.con)
            except:
                df = pd.DataFrame()
                df.to_sql(self.table, con=self.con, if_exists="append")
                self.df = pd.read_sql(self.table, con=self.con)
        else:
            print('Error: Koneksi ke DB gagal!')
    def add_data(self, bucket):
        df_new = pd.DataFrame()
        for i in bucket:
            shortcode = i['shortcode']
            dfc = pd.read_sql_query("""SELECT * FROM """ + self.table + """ WHERE shortcode """ + shortcode, con=con)
            if len(dfc)!=0:
                dfx = pd.DataFrame(i)
                df_new = df_new.append(dfx)
        df_new.to_sql(self.table,con=self.con, if_exists='append')
    def get_df(self):
        self.df = pd.read_sql(self.table, con=self.con)
        return self.df