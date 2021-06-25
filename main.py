from time import sleep
import mysql.connector
from rich.prompt import Confirm, Prompt
from rich.console import Console
from rich.table import Table
from rich import print
from rich.panel import Panel
from rich.progress import track
import re

db = mysql.connector.connect(host='192.168.86.38',
                             user='marvel',
                             password='starwars285',
                             db='personal')

c = db.cursor()


def format(string: str) -> str:
    pattern = r'[(),\']'
    string = re.sub(pattern, '', str(string))

    return string


def insert():
    choices = []
    info = []
    progress = []

    console = Console()

    c.execute("SHOW TABLES")
    for i in c:
        i = format(i)
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

            progress.append(j)

            data = str(input(f'{j}:'))
            info.append(data)

        c.execute(
            "INSERT INTO " + table +
            " (`first name`, `last name`, `email`, `discord`, `birthday`, `notes`) VALUES (%s, %s, %s, %s, %s, %s)",
            (info[0], info[1], info[2], info[3], info[4], info[5]),
        )

        db.commit()

        with console.status("[dark green] Inserting...") as status:
            while progress:
                task = progress.pop(0)
                sleep(1)
                print(f"Inserted {task} [underline bold green]successfully[/underline bold green]!")

def view():
    choices = []

    c.execute("SHOW TABLES")
    for i in c:
        i = format(i)
        choices.append(str(i))

    table = Prompt.ask("What table do you want to view the data for?",
                       choices=choices)

    grid = Table(title=table, show_lines=True)
    c.execute("SHOW COLUMNS FROM " + table)

    for column in c:
        column = format(column[0])
        grid.add_column(column, justify='center')

    c.execute("SELECT * FROM " + table)

    for data in c:

        data = list(data)

        grid_values = []

        for i in data:
            i = format(i)
            grid_values.append(i)

        grid.add_row(*grid_values)

    console = Console()
    console.print(grid)
    return table


def delete():
    data = []
    table = view()

    c.execute("SELECT id FROM " + table)

    for i in c:
        i = str(i)
        data.append(i)

    print("[bold red] Which row do you want to delete: ")

    for i in data:
        i = format(i)
        print(Panel(str(i)))

    del_row = str(input("Choice: "))

    ok = Confirm.ask("Are you sure you want to delete row {}".format(del_row))

    try:
        assert ok

        c.execute("DELETE FROM contacts WHERE id={}".format(del_row))

        for _ in track(range(100), description='Deleting...'):
            sleep(0.03)

        db.commit()

    except AssertionError:
        exit()


while __name__ == "__main__":
    wut = Prompt.ask("What do you want to do?:",
                     choices=['view', 'insert', 'delete', 'exit'])

    if wut.lower() == 'view':
        view()
        sleep(1)

    elif wut.lower() == 'insert':
        insert()
        sleep(1)

    elif wut.lower() == 'delete':
        delete()
        sleep(1)

    elif wut.lower() == 'exit':
        exit()
