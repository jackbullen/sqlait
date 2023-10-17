# SQLait

Retrieve DBMS schema over SSH and generate queries with GPT.

## Usage

1. Clone the repo

2. Install python dependencies: `dotenv`, `psycopg2`, and `sshtunnel`

3. Setup env variables. Requires SSH (host, port, username, password), PostgreSQL database (db name, port, hostname, user, password), and OpenAI API key

4. Run `main.py`