from mysql import connector


def execute(conn: "Connection",
            sql: str, fetch_one=False) -> list[tuple] | None:
    print("Executing:", sql)
    conn.cursor.execute(sql, multi=True)
    response = conn.cursor.fetchone() if fetch_one else conn.cursor.fetchall()
    conn.cursor.reset()
    print("return resonse:", response)
    return response


class Connection:
    def __init__(self, database) -> None:
        config = {
            "user": "root",
            "password": "root",
            "host": "database",
            "port": "3306"
        }
        if database is not None:
            config["database"] = database
        self.connection = connector.connect(**config)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()


class Database:

    database: str = None
    connection: Connection = None

    def connect(self, database: str):
        self.database = database
        self.connection = Connection(database)

    def create_new_database(self, new_database: str):
        connection = Connection(None)
        execute(connection, f"CREATE DATABASE IF NOT EXISTS {new_database}")
        self.connection = Connection(new_database)

    def execute_text(self, sql: str, fetch_one: bool):
        return execute(self.connection, sql, fetch_one)

    def execute_file(self, filepath: str, fetch_one: bool):
        commands = [command for command in open(
            filepath, "r").read().replace("\n", "").split(";")]
        responses = [self.execute_text(command, fetch_one)
                     for command in commands]
        return responses
