import sqlite3
conn = sqlite3.connect('words.db')
c = conn.cursor()
c.execute('''CREATE TABLE words (id INTEGER PRIMARY KEY, rank INTEGER, word TEXT, part_of_speech TEXT, frequency INTEGER)''')


f = open("Common-English-Words.csv","r")
text = f.read()
text = text.splitlines()
table = []
for lines in text:
  table.append(lines.split(","))
  
#Rank,Word,Part of speech,Frequency,Dispersion
for rows in table:
  rank = rows[0]
  word = rows[1]
  part = rows[2]
  freq = rows[3]
  row = (rank, word, part, freq)
  c.execute("INSERT INTO words VALUES(null,?,?,?,?)",row)
  
conn.commit()
conn.close()