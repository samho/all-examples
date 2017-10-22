import sqlite3
import cPickle
import marshal

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS image(id INTEGER PRIMARY KEY AUTOINCREMENT,image BLOB, FILE_NAME TEXT)""")
with open('SNoti2.png', "rb") as input_file:
    bablob = marshal.dumps(input_file.read(), 2)
    cur.execute('INSERT INTO image(image) VALUES (?)', [sqlite3.Binary(bablob)])

with open("test2.png", 'wb') as output_file:
    cur.execute('SELECT image from image limit 1')
    ablob = cur.fetchone()
    bablob = marshal.loads(ablob[0])
    output_file.write(bablob)

con.commit()
con.close()