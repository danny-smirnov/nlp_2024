import json
import psycopg2
from psycopg2.extras import execute_values
import os
from tqdm import tqdm

DB_CONFIG = {
    "dbname": "wikisearch",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}

TABLE_NAME = "wiki_headers"
COLUMNS = ["id", "url", "title", "embedding"]

def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_data_to_pgvector(rows, batch_size=100000):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        vals_str = ", ".join(["%({0})s".format(x) for x in COLUMNS])
        query = f"""
            INSERT INTO {TABLE_NAME} ({", ".join(COLUMNS)})
            VALUES %s
        """
        for i in tqdm(range(0, len(rows), batch_size)):
            batch = rows[i:i + batch_size]
            values = [(row['id'], row['url'], row['title'], row['embedding']) for row in batch]
            execute_values(cursor, query, values)
            conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_closest(emb):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        query = f"""
            SELECT *, 1 - (embedding <=> %s::vector) AS cosine_similarity FROM wiki_headers ORDER BY cosine_similarity DESC LIMIT 10;
        """
        
        cursor.execute(query, (emb.tolist(),))
        data = cursor.fetchall()
        return [(x[2], x[1]) for x in data]
        
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    data_dir = 'D:/tasks/task3/data/vectorized_titles'
    for filename in os.listdir(data_dir):
        print(f"Data insertion of {filename}")

        filepath = os.path.join(data_dir, filename)
        data = read_json_file(filepath)
        insert_data_to_pgvector(data)
