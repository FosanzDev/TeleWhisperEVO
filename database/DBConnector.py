import psycopg2
from .__languages import languages


class DBConnector:

    def __init__(self, host, port, database, username, password):
        self.conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=host,
            port=port,
            sslmode="require"
        )
        self.cursor = self.conn.cursor()
        self.__init_db()

    def __init_db(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "user_id INT PRIMARY KEY,"
            "user_name TEXT,"
            "balance INT DEFAULT 0,"
            "superuser BOOLEAN DEFAULT FALSE,"
            "admin BOOLEAN DEFAULT FALSE,"
            "banned BOOLEAN DEFAULT FALSE,"
            "language TEXT DEFAULT 'none'"
            ");")

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS actions ("
            "action_id SERIAL PRIMARY KEY,"
            "user_id INT,"
            "action TEXT,"
            "length INT,"
            "cost INT,"
            "status TEXT DEFAULT 'pending',"
            "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "FOREIGN KEY (user_id) REFERENCES users(user_id)"
            ");")

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS transactions ("
            "transaction_id SERIAL PRIMARY KEY,"
            "user_id INT,"
            "currency TEXT,"
            "amount INT,"
            "balance INT,"
            "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "FOREIGN KEY (user_id) REFERENCES users(user_id)"
            ");"
        )

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS languages ("
            "language TEXT PRIMARY KEY,"
            "name TEXT"
            ");"
        )

        for iso_code, name in languages.items():
            self.cursor.execute(
                "INSERT INTO languages (language, name) VALUES (%s, %s) "
                "ON CONFLICT (language) DO NOTHING;",
                (iso_code, name)
            )

        self.conn.commit()

    async def register(self, user_id, user_name):
        self.cursor.execute(
            "INSERT INTO users (user_id, user_name) VALUES (%s, %s) "
            "ON CONFLICT (user_id) DO NOTHING;",
            (user_id, user_name)
        )
        self.conn.commit()

    async def get_user(self, user_id) -> tuple | None:
        self.cursor.execute(
            "SELECT * FROM users WHERE user_id = %s;",
            (user_id,)
        )
        return self.cursor.fetchone()

    async def register_action(self, user_id, action, length, cost):
        self.cursor.execute(
            "INSERT INTO actions (user_id, action, length, cost) VALUES (%s, %s, %s, %s);",
            (user_id, action, length, cost)
        )

        self.cursor.execute(
            "UPDATE users SET balance = balance - %s WHERE user_id = %s;",
            (cost, user_id)
        )

        self.conn.commit()

    async def register_transaction(self, user_id, currency, amount, balance):
        self.cursor.execute(
            "INSERT INTO transactions (user_id, currency, amount, balance) VALUES (%s, %s, %s, %s);",
            (user_id, currency, amount, balance)
        )

        self.cursor.execute(
            "UPDATE users SET balance = balance + %s WHERE user_id = %s;",
            (amount, user_id)
        )

        self.conn.commit()