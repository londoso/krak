#!/usr/bin/python
import psycopg2
from load_db_config import config
import s3fs
import os
import pandas as pd
from io import StringIO

def copy_csv():
    """ Copy CSV File Into PostgreSql Table """
    conn = None
    try:
        # Open Connection
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute('SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();')
        cur.execute('truncate table repo.indicador restart identity;')

        bucket = os.environ['bucket']
        df = pd.read_csv('s3://' + bucket + '/EdStatsData.csv', sep=',', usecols=['Country Name','Indicator Name','2016','2017'], index_col=False)
        print('>> Main Dataframe <<')
        print(df.count())
        print(df.head())        
        ser = df.melt(id_vars=['Country Name','Indicator Name'], var_name='year')
        print('>> Melt Dataframe <<')
        print(ser.count())
        print(ser.head())       
        csv_io = StringIO()
        ser.to_csv(csv_io, header=True, index=False)
        csv_io.seek(0)
        cur.copy_expert('COPY repo.indicador FROM STDIN WITH DELIMITER \',\' CSV HEADER', csv_io, size=8192)
        cur.copy_expert('COPY repo.indicador (COUNTRYNAME, INDICATORNAME, YEAR, VALUE) FROM STDIN WITH CSV HEADER', csv_io, size=8192)
        print()
        print('  ' + str(cur.rowcount) + ' Rows loaded from CSV')
        print()
        conn.commit()

        #cur.execute("select * from repo.indicador;")  
        #db_output = cur.fetchone()
        #db_output = cur.fetchall()
        #print(db_output)
       
        # Close Connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    copy_csv()