import os
import json

import psycopg2


class PostgresUtils:
    def __init__(self):
        """
        Read the config file and get the credentials and initialize the postgres connection
        :except: Exception, if any exception occurs, it will be printed on the screen
        """
        try:
            config_folder = os.path.join(os.path.expanduser("~"), ".pwd_mgr")
            config_file = os.path.join(config_folder, "config.json")
            with open(config_file, "r") as f:
                config = f.read()
                config = json.loads(config)
            self.conn = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"],
                options=f"-c search_path={config['search_path']}"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise Exception(e)

    def execute_query(self, query, to_return=False):
        """
        Execute the query and to_return is to indicate the query is select where cur will return results.
        :param query: the SQL query to execute
        :param to_return: Flag to indicate the query is select where cur will return results.
        :return: if to_return is True, it will return the result of the query else None
        :except: Exception, if any exception occurs, it will be printed on the screen
        """
        try:
            self.cursor.execute(query)
            if to_return:
                return self.cursor.fetchall()
            self.conn.commit()
        except Exception as e:
            raise Exception(e)

    def close_connection(self):
        """
        Close the connection
        :except: Exception, if any exception occurs, it will be printed on the screen
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            raise Exception(e)
