import re
import hashlib

def sanitize_filename(user_input, max_length=20):
    sanitized = re.sub(r'[^a-zA-Z0-9]', '_', user_input)
    
    short_name = sanitized[:max_length]
    input_hash = hashlib.md5(user_input.encode()).hexdigest()[:8]
    
    return f"{short_name}_{input_hash}.sql"

def store_data(query_title, sql_query, query_response):
    filename = sanitize_filename(query_title)
    with open('queries/'+filename, "w") as f:
        f.write(f"-- Query: {query_title}\n\n")
        f.write(f"-- Response: {query_response}\n\n")
        f.write(f"{sql_query}")
    return filename