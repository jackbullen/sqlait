#!/usr/bin/env python3

from db_connection import connect_to_db, fetch_schema_information, close_tunnel, execute_query
from generate_query import generate_sql_query
from cache import store_data

def main():
    connection, tunnel = connect_to_db()

    schema_info = fetch_schema_information(connection)
    schema_msg = ""
    for table in schema_info:
        schema_msg += f"Table {table} has attributes: {schema_info[table]}\n"

    user_input = input("Please describe the query you want to execute: ")
    messages = [{"role": "system", "content": "Act as database expert and generate SQL queries. \
                 Only access attributes on the tables as they are given in the schema. \
                 User may specify constraints on what is allowed in SQL query. \
                 Place the sql inside of ```sql``` code cell."}, 
                 {"role": "user", "content": f"Given the database schema\n {schema_msg}\n\n \
                  Convert this request: '{user_input}'"}]

    retry_count = 0
    MAX_RETRIES = 0
    while retry_count < MAX_RETRIES+1:
        for message in messages:
            print(f"{message['role']}: {message['content']}\n\n")
        print("-"*27)
        sql_query, message = generate_sql_query(messages)
        messages.append(message)
        print(sql_query)
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            if not results:
                try_again = input("No results found. Try again? (y/n): ")
                if try_again == "y":
                    retry_count += 1
                    messages.append({"role": "user", "content": "No results were found, however, there should be results. \
                        Please try again with a different approach following the constraints if there are any."})
                    continue
                else:
                    exit()
            break
        except Exception as e:
            retry_count += 1
            print(f"Retry {retry_count}: Error on executing query: {e}")
            messages.append({"role": "user", "content": f"Error executing query: {e}"})
        finally:
            cursor.close()

        if retry_count == MAX_RETRIES:
            raise Exception("Max retries exceeded. Please try again.")

    results = execute_query(connection, sql_query)
    print("Results:")
    for row in results:
        print(row)

    filename = store_data(user_input, sql_query, results)
    print(f"Data stored in {filename}")

    connection.close()
    close_tunnel(tunnel)

if __name__ == "__main__":
    main()