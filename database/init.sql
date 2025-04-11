CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY ,
    user_name TEXT,
    balance INT DEFAULT 0,
    superuser BOOLEAN DEFAULT FALSE,
    admin BOOLEAN DEFAULT FALSE,
    banned BOOLEAN DEFAULT FALSE,
    language TEXT DEFAULT 'none',
    transcription_provider TEXT DEFAULT 'runpod',
    translation_provider TEXT DEFAULT 'deepl'
);

CREATE TABLE IF NOT EXISTS actions (
    action_id SERIAL PRIMARY KEY,
    user_id INT,
    action TEXT,
    lenght INT,
    cost INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT,
    amount INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS errors (
    error_id UUID PRIMARY KEY,
    user_id INT,
    action TEXT,
    error TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS languages (
    language TEXT PRIMARY KEY,
    name TEXT
);