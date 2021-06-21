import mysql.connector
from rich.prompt import Prompt
import re

db = mysql.connector.connect(host='192.168.86.38',
                             user='marvel',
                             password='starwars285',
                             db='personal')

c = db.cursor()


def insert():
    choices = []
    info = []
    c.execute("SHOW TABLES")
    for i in c:
        pattern = r'[(),\']'
        i = re.sub(pattern, '', str(i))
        choices.append(str(i))

    table = Prompt.ask("What table do you want to insert data into?",
                       choices=choices)

    print("Enter the needed information:")

    c.execute("SHOW COLUMNS FROM contacts")
    for i in c:
        j = i[0]

        if j == 'id':
            break

        data = str(input(f'{j}:'))
        info.append(data)

    c.execute(
        "INSERT INTO " + table +
        " (`first name`, `last name`, `email`, `discord`, `birthday`, `notes`) VALUES (%s, %s, %s, %s, %s, %s)",
        (info[0], info[1], info[2], info[3], info[4], info[5]),
    )

    db.commit()


insert()
