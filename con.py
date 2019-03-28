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
            print('Koneksi berhasil', table)
        except:
            print('Error: Koneksi ke DB gagal!')

    def add_data(self, bucket):
        bucket_new = []
        for i in bucket:
            shortcode = i['shortcode']
            try:
                dfc = pd.read_sql_query("""SELECT * FROM """ + self.table + """ WHERE shortcode = '""" + shortcode + "'", con=self.con)
                if len(dfc)==0:
                    bucket_new.append(i)
                else:
                    print(shortcode, 'ada')
            except:
                bucket_new.append(i)
        if len(bucket_new) != 0:
            df_new = pd.DataFrame(bucket_new)
            # print(df_new)
            df_new.to_sql(self.table,con=self.con, if_exists='append')
        print('table:', self.table, str(len(bucket_new)))

    def get_df(self):
        df = pd.read_sql(self.table, con=self.con)
        return df
    def close(self):
        self.con.close()