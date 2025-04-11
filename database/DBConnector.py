import psycopg2
from .__languages import languages

class DBConnector:

    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None
        self.connect()


    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.database,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            sslmode="require"
        )
        self.cursor = self.conn.cursor()
        self.__init_db()

    def __init_db(self):
        try:
            with open('database/init.sql', 'r') as file:
                self.cursor.execute(file.read())

            for lang in languages.keys():
                if lang == 'none':
                    continue
                name = languages[lang].get('label')
                self.cursor.execute(
                    "INSERT INTO languages (language, name) VALUES (%s, %s) "
                    "ON CONFLICT (language) DO NOTHING;",
                    (lang, name)
                )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def reconnect(self):
        if self.conn.closed:
            self.connect()

    def execute_query(self, query, params):
        self.reconnect()
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.connect()
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def fetch_query(self, query, params):
        self.reconnect()
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except (psycopg2.OperationalError, psycopg2.InterfaceError):
            self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            self.conn.rollback()
            raise e

    def register(self, user_id, user_name):
        self.execute_query(
            "INSERT INTO users (user_id, user_name) VALUES (%s, %s) "
            "ON CONFLICT (user_id) DO NOTHING;",
            (user_id, user_name)
        )

    def get_user(self, user_id) -> tuple | None:
        return self.fetch_query(
            "SELECT * FROM users WHERE user_id = %s;",
            (user_id,)
        )

    def is_privileged(self, user_id) -> bool:
        user = self.get_user(user_id)
        return user[3] or user[4]

    def get_credits(self, user_id) -> int:
        result = self.fetch_query(
            "SELECT balance FROM users WHERE user_id = %s;",
            (user_id,)
        )
        return result[0] if result else 0

    def register_action(self, user_id, action, length, cost):
        if self.is_privileged(user_id):
            cost = 0
        self.execute_query(
            "INSERT INTO actions (user_id, action, length, cost) VALUES (%s, %s, %s, %s);",
            (user_id, action, length, cost)
        )
        self.execute_query(
            "UPDATE users SET balance = balance - %s WHERE user_id = %s;",
            (cost, user_id)
        )

    def register_transaction(self, user_id, amount):
        self.execute_query(
            "INSERT INTO transactions (user_id, amount) VALUES (%s, %s);",
            (user_id, amount)
        )
        self.execute_query(
            "UPDATE users SET balance = balance + %s WHERE user_id = %s;",
            (amount, user_id)
        )

    def register_error(self, error_id, user_id, action, error):
        self.execute_query(
            "INSERT INTO errors (error_id, user_id, action, error) VALUES (%s, %s, %s, %s);",
            (str(error_id), user_id, action, error)
        )

    def get_language(self, user_id) -> str:
        result = self.fetch_query(
            "SELECT language FROM users WHERE user_id = %s;",
            (user_id,)
        )
        return result[0] if result else 'none'

    def set_language(self, user_id, language):
        self.execute_query(
            "UPDATE users SET language = %s WHERE user_id = %s;",
            (language, user_id)
        )

    def get_user_translation_provider(self, user_id: str) -> str:
        result = self.fetch_query(
            "SELECT translation_provider FROM users WHERE user_id = %s;",
            (user_id,)
        )
        return result[0] if result else None

    def get_user_transcription_provider(self, user_id: str) -> str:
         result =  self.fetch_query(
            "SELECT transcription_provider FROM users WHERE user_id = %s;",
            (user_id,)
        )
         return result[0] if result else None
