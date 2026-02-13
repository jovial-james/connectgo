import mysql.connector
try:
    conn=mysql.connector.connect(host='localhost',user="root",password="mysql",database='connectGo')
    cursor = conn.cursor()

    #create tables
    cursor.execute("""Create database User(
                   userid int primary key auto_increment,
                   username varchar(15) not null,
                   pswd varchar(20)
                   )""")