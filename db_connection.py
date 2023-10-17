from sshtunnel import SSHTunnelForwarder
import psycopg2
import dotenv
import os

dotenv.load_dotenv()

SSH_HOST = os.getenv("SSH_HOST")
SSH_PORT = int(os.getenv("SSH_PORT"))
SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")

REMOTE_DB_HOST = os.getenv("REMOTE_DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def create_tunnel():
    tunnel = SSHTunnelForwarder(
        (str(SSH_HOST), SSH_PORT),
        ssh_username=SSH_USER,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(REMOTE_DB_HOST, DB_PORT)
    )
    tunnel.start()
    return tunnel

def connect_to_db():
    tunnel = create_tunnel()
    print("Connecting to database...")
    connection = psycopg2.connect(
        host=DB_HOST,
        port=tunnel.local_bind_port,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connected to database!")
    return connection, tunnel

def fetch_schema_information(connection):
    cursor = connection.cursor()

    cursor.execute("select datname from pg_database;")
    databases = cursor.fetchall()
    schema_info = {'db': databases, 'tables': {}}
 
    cursor.execute("select table_name from information_schema.tables where table_schema='public';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"select * from {table_name} limit 1;")
        columns = [desc[0] for desc in cursor.description]
        schema_info['tables'][table_name] = columns
    
    cursor.close()

    return schema_info['tables']

def execute_query(connection, query):
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()

    return results

def close_tunnel(tunnel):
    tunnel.stop()