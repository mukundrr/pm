import os
import json
import uuid
from pm.utils import pg_utils
from rich import table
from rich import console

console_ = console.Console()


def check_pg_config():
    """
    Check if the postgres configuration file exists in the home directory.
    If not, exit the program.
    :return: exit with status 1 if the file does not exist, else return None
    :except: Exception, if any exception occurs, it will be printed on the screen and exit with status 1
    """
    try:
        root_directory = os.path.expanduser("~")
        config_file = os.path.join(root_directory, ".pwd_mgr")
        if not os.path.exists(config_file):
            console_.print("Postgres configuration not found", style="red")
            exit(1)
    except Exception as e:
        console_.print(e, style="red")
        exit(1)


def configure_pg():
    """
    Configure the postgres connection details and save it in the home directory.
    it will create a folder .pwd_mgr in the home directory and save the configuration in a file named config.json
    expected keys in the configuration are host, port, user, password, database, search_path
    :return: None, A console message will be printed on the screen
    :except: Exception, if any exception occurs, it will be printed on the screen
    """
    try:
        root_directory = os.path.expanduser("~")
        config_folder = os.path.join(root_directory, ".pwd_mgr")
        if not os.path.exists(config_folder):
            os.makedirs(config_folder, exist_ok=True)
        config_file = os.path.join(config_folder, "config.json")
        host = input("Enter the host: ")
        port = input("Enter the port: ")
        user = input("Enter the user: ")
        password = input("Enter the password: ")
        database = input("Enter the database: ")
        search_path = input("Enter the search path: ")
        config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "search_path": search_path
        }
        with open(config_file, "w") as f:
            f.write(json.dumps(config))
        console_.print("Configuration saved successfully", style="green")
    except Exception as e:
        console_.print(e, style="red")


def list_credentials():
    """
    List all the credentials saved in the database
    :return: None, A console message will be printed on the screen
    :except: Exception, if any exception occurs, it will be printed on the screen
    """
    try:
        check_pg_config()
        pg_utils_ = pg_utils.PostgresUtils()
        query = "SELECT * FROM pwd_mgr;"
        result = pg_utils_.execute_query(query, to_return=True)
        table_ = table.Table(title="Credentials", style="green")
        table_.add_column("id", style="white", overflow="fold")
        table_.add_column("website", style="cyan", overflow="fold")
        table_.add_column("email", style="magenta", overflow="fold")
        table_.add_column("password", style="yellow", overflow="fold")
        if len(result) == 0:
            console_.print("No credentials found", style="yellow")
            return
        for row in result:
            table_.add_row(row[3], row[0], row[1], row[2])
        console_.print(table_)
        pg_utils_.close_connection()
    except Exception as e:
        console_.print(e, style="red")


def save_credentials(website, email, password):
    """
    Save the credentials in the database
    :param website: name of the website for which the credentials are saved
    :param email: user email
    :param password: password
    :return: None, A console message will be printed on the screen
    :except: Exception, if any exception occurs, it will be printed on the screen
    """
    try:
        check_pg_config()
        pg_utils_ = pg_utils.PostgresUtils()
        id_ = uuid.uuid4()
        query = (f"INSERT INTO pwd_mgr (id, website, email, password) "
                 f"VALUES ('{id_}', '{website}', '{email}', '{password}');")
        pg_utils_.execute_query(query)
        console_.print("Credentials saved successfully", style="green")
        pg_utils_.close_connection()
    except Exception as e:
        console_.print(e, style="red")


def delete_credentials(id_):
    """
    Delete the credentials from the database
    :param id_: the id of the credentials to delete
    :return: None, A console message will be printed on the screen
    :except: Exception, if any exception occurs, it will be printed on the screen
    """
    try:
        check_pg_config()
        pg_utils_ = pg_utils.PostgresUtils()
        query = f"DELETE FROM pwd_mgr WHERE id = '{id_}';"
        pg_utils_.execute_query(query)
        console_.print("Credentials deleted successfully", style="green")
        pg_utils_.close_connection()
    except Exception as e:
        console_.print(e, style="red")


def update_credentials(id_, website=None, email=None, password=None):
    """
    Update the credentials in the database
    :param id_: the id of the credentials to update
    :param website: name of the website for which the credentials are saved
    :param email: user email
    :param password: password
    :return: None, A console message will be printed on the screen
    :except: Exception, if any exception occurs, it will be printed on the screen
    """
    try:
        try:
            uuid.UUID(id_)
        except ValueError:
            console_.print("Invalid id", style="red")
            return
        check_pg_config()
        pg_utils_ = pg_utils.PostgresUtils()
        query = f"SELECT * FROM pwd_mgr WHERE id = '{id_}';"
        result = pg_utils_.execute_query(query, to_return=True)
        if len(result) == 0:
            console_.print("Invalid id", style="red")
            return
        query = "update pwd_mgr set "
        is_update = False
        if website:
            query += f"website = '{website}', "
            is_update = True
        if email:
            query += f"email = '{email}', "
            is_update = True
        if password:
            query += f"password = '{password}', "
            is_update = True
        if not is_update:
            console_.print("Nothing to update", style="yellow")
            return
        query = query[:-2] + f" WHERE id = '{id_}';"
        pg_utils_.execute_query(query)
        console_.print("Credentials updated successfully", style="green")
        pg_utils_.close_connection()
    except Exception as e:
        console_.print(e, style="red")
