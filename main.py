#!/usr/bin/env python3

from db_connection import connect_to_db, fetch_schema_information, close_tunnel, execute_query
from generate_query import generate_sql_query
from cache import store_data

def main():
    connection, tunnel = connect_to_db()
    schema_info = fetch_schema_information(connection)
    
    user_input = input("Please describe the query you want to execute: ")
    messages = [{"role": "system", "content": "Act as a database expert and generate the SQL queries. \
                 The user may specify constraints on what is allowed in the SQL query. \
                 Provide only the query using professional modern database retrieval methods. \
                 Do not provide ```sql``` around the response, do not apologize for incorrect responses, simply ONLY respond with SQL that can be pasted into psql. Only include the raw SQL as text and nothing else as I will feed this directly to PSQL."}, 
                 {"role": "user", "content": f"Given the database schema {schema_info}, \
                  convert the user request '{user_input}' into an SQL query. \Provide only the SQL query."}]

    retry_count = 0
    MAX_RETRIES = 3
    while retry_count < MAX_RETRIES:
        gpt_response = generate_sql_query(messages)
        sql_query = gpt_response["choices"][0]["message"]["content"]
        print(sql_query)

        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            break
        except Exception as e:
            retry_count += 1
            print(f"Retry {retry_count}: Error on executing query: {e}")
            messages.append({"role": "system", "content": sql_query})
            messages.append({"role": "user", "content": f"Error executing query: {e}"})
            gpt_response = generate_sql_query(messages)
            sql_query = gpt_response["choices"][0]["message"]["content"]
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