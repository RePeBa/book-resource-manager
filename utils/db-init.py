import sqlite3

conn = sqlite3.connect('../books.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS book( id integer primary key, author text, title text) """)

c.execute("SELECT * FROM book")

print(c.fetchall())

conn.commit()

conn.close()







