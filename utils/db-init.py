import sqlite3

conn = sqlite3.connect('../dbase.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS book( id integer primary key, author text, title text) """)
c.execute("SELECT * FROM book")
c.execute("""CREATE TABLE IF NOT EXISTS user( id integer primary key, username text, email text, password text) """)
c.execute("SELECT * FROM user")

conn.commit()
conn.close()







