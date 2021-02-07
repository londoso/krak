import psycopg2
import s3fs
import pandas as pd
from io import StringIO

conn = psycopg2.connect(
    host="master.caanqvphypwt.us-east-1.rds.amazonaws.com",
    database="krak",
    user="anderson",
    password="pasS123crak")
	
cur = conn.cursor()
cur.execute('SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE datname = current_database() AND pid <> pg_backend_pid();')
cur.execute('truncate table repo.usuario;')

df = pd.read_csv('s3://sdsadf-s3bucket-1c0n4owkq66ya/test.csv', sep=',', usecols=['id', 'nombre'], index_col=False)
csv_io = StringIO()
df.to_csv(csv_io, header=False, index=False)
csv_io.seek(0)
cur.copy_expert('COPY repo.usuario FROM STDIN WITH DELIMITER \',\' CSV HEADER', csv_io, size=8192)
conn.commit()

cur.execute("select * from repo.usuario;")
cur.fetchall()

cur.close()

