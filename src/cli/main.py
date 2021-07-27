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

# MISC FUNCTIONS


def format(string: str) -> str:
    """
    Removes uneeded characters using regex

    Args:
        string (str): The string the needs characters removed

    Returns:
        str: The new string without any of the uneeded characters
    """
    pattern = r'[(),\']'
    string = re.sub(pattern, '', str(string))

    return string


# DATA OPERATION FUNCTIONS


def insert():
    """
    Inserts data into a table
    """
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

        with console.status("[dark green] Inserting..."):
            while progress:
                task = progress.pop(0)
                sleep(1)
                print(
                    f"Inserted {task} [underline bold green]successfully[/underline bold green]!"
                )


def view():
    """
    Views data from a selected table in the form of a table 
    """
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
    """
    Deletes data from a selected table
    """
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


def sort():
    """
    Sorts given data using the mysql `ORDER BY` statement
    """
    choices = []
    columns = []

    c.execute("SHOW TABLES")
    for i in c:
        i = format(i)
        choices.append(str(i))

    table = Prompt.ask("What table do you want to view the data for?",
                       choices=choices)

    c.execute("SHOW COLUMNS FROM " + table)

    for column in c:
        column = format(column[0])
        columns.append(column)

    sort_column = Prompt.ask('Which column do you want to sort by?',
                             choices=columns)
    sort_way = Prompt.ask('Would you like to sort ascending or descending?',
                          choices=['asc', 'desc'])

    grid = Table(title=table, show_lines=True)
    c.execute("SHOW COLUMNS FROM " + table)

    for column in c:
        column = format(column[0])
        grid.add_column(column, justify='center')

    c.execute('SELECT * FROM {} ORDER BY `{}` {}'.format(
        table, sort_column, sort_way))

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


def edit():
    """
    Edit a specific piece of data based on its id and column
    """
    ids = []
    columns = []
    table = view()

    c.execute("SELECT `id` FROM {}".format(table))
    for id in c:
        id = format(id[0])
        ids.append(id)

    c.execute("SHOW COLUMNS FROM " + table)

    for column in c:
        column = format(column[0])
        if column == 'id': break
        columns.append(column)

    row_id = Prompt.ask('What is the id of the row you want to edit?',
                        choices=ids)
    col = Prompt.ask('Which column do you want to edit?', choices=columns)
    new_val = str(input('What is the new value: '))

    c.execute('UPDATE {} SET `{}` = \'{}\' WHERE `id` = {}'.format(
        table, col, new_val, row_id))
    db.commit()


while __name__ == "__main__":
    wut = Prompt.ask(
        "What do you want to do?:",
        choices=['view', 'insert', 'delete', 'sort', 'edit', 'exit'])

    if wut.lower() == 'view':
        view()
        sleep(1)

    elif wut.lower() == 'insert':
        insert()
        sleep(1)

    elif wut.lower() == 'delete':
        delete()
        sleep(1)

    elif wut.lower() == 'sort':
        sort()
        sleep(1)

    elif wut.lower() == 'edit':
        edit()
        sleep(1)

    elif wut.lower() == 'exit':
        exit()
