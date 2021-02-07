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
        cur.execute('truncate table repo.usuario;')

        bucket = os.environ['bucket']
        df = pd.read_csv('s3://' + bucket + '/test.csv', sep=',', usecols=['id', 'nombre'], index_col=False)
        csv_io = StringIO()
        df.to_csv(csv_io, header=False, index=False)
        csv_io.seek(0)
        cur.copy_expert('COPY repo.usuario FROM STDIN WITH DELIMITER \',\' CSV HEADER', csv_io, size=8192)
        conn.commit()

        cur.execute("select * from repo.usuario;")
        cur.fetchall()

        db_output = cur.fetchall()
        print(db_output)
       
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