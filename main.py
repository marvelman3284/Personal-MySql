import mysql.connector
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
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

    if table == 'contacts':

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


def view():
    choices = []

    c.execute("SHOW TABLES")
    for i in c:
        pattern = r'[(),\']'
        i = re.sub(pattern, '', str(i))
        choices.append(str(i))

    table = Prompt.ask("What table do you want to view the data for?",
                       choices=choices)

    grid = Table(title=table, show_lines=True)
    c.execute("SHOW COLUMNS FROM " + table)

    for column in c:
        pattern = r'[(),\']'
        column = re.sub(pattern, '', str(column[0]))
        grid.add_column(column, justify='center')

    c.execute("SELECT * FROM " + table)
    for data in c:
        grid.add_row(str(*data))

    console = Console()
    console.print(grid)


if __name__ == "__main__":
    wut = input("What do you want to do (view or insert data):")

    if wut.lower() == 'view':
        view()
    elif wut.lower() == 'insert':
        insert()
