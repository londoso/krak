#!/usr/bin/python
import psycopg2
from load_db_config import config

def create_env():
    """ Copy CSV File Into PostgreSql Table """
    conn = None
    try:
        # Open Connection
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute('drop schema repo if exists cascade;')
        cur.execute('create schema repo if not exists;')
        #cur.execute('drop table if exists repo.usuario;')
        cur.execute('create table if not exists repo.usuario (id integer, nombre varchar);')

        print('Env repo.usuario Created')
       
        # Close Connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    create_env()