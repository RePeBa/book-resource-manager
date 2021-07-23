import sqlite3

conn = sqlite3.connect('../dbase.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS books( id integer primary key, author text, title text) """)
c.execute("""CREATE TABLE IF NOT EXISTS users( id integer primary key,  text, title text) """)

# c.execute("""CREATE TABLE IF NOT EXISTS users( id integer primary key, username text, email text, password text) """)
# c.execute("""CREATE TABLE IF NOT EXISTS roles( id integer primary key, name text) """)

conn.commit()
conn.close()







