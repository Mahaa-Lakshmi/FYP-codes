import sqlite3
db=sqlite3.connect('User.db')
cursor=db.cursor()
#cursor.execute("create table UserRegTable(email text primary key,carbrand text,modelname text,password text)")
#db.commit()
#cursor.execute("INSERT INTO UserRegTable(email,carbrand,modelname,password) VALUES(?, ?, ?,?)",('maha','Volvo','i20','mahpwd') )
cursor.execute("SELECT * FROM UserRegTable")
all_rows = cursor.fetchall()
db.commit()
for row in all_rows:
    print(row)
