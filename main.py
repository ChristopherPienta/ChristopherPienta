import sqlite3

#connect creates a connection to the data base file
conn = sqlite3.connect('ihub.db')

#cursor allows you to execut sql commands
cur = conn.cursor()

#by useing triple quotes we can write multi-line strings aka string literal
 cur.execute("""
      CREATE TABLE if not exists ihub_table
      (
          User TEXT,
          Ticker TEXT,
          Market_Cap TEXT,
          Authorized_Shares TEXT,
          Outstanding_Shares TEXT,
          Restricted TEXT,
          Unrestricted TEXT,
          Held_At_DTC TEXT,
          Float TEXT,
          Date DATE
      )
     """)
commit adds the data to the multi user enviornment so others can see your work
conn.commit()

 post = [
     ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
 ]
executemany creates an iterator for the multiple entires in the many_samples variable
cur.executemany("INSERT INTO ihub_table values(?,?,?,?,?,?,?,?,?,?)", post)
conn.commit()


cur.execute("SELECT * FROM ihub_table")

results = cur.fetchall()
#results = cur.fetchmany(2)
#results = cur.fetchone()

if results != None:
    for r in results:
        print(r)

conn.close();