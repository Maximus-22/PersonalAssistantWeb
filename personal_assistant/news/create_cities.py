import json
import psycopg2


def read_json_data(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        data = json.load(file)
    return data['cities']


def write_to_postgres(data, conn):
    cur = conn.cursor()
    for row in data:
        cur.execute("""
            INSERT INTO news_city (name, latitude, longitude)
            VALUES (%(name)s, %(latitude)s, %(longitude)s)
        """, row)
    conn.commit()
    cur.close()

json_file_path = 'cities.json'

# conn = psycopg2.connect(database="your_database", user="your_username", password="your_password", host="127.0.0.1", port="5432")
conn = psycopg2.connect(database="", user="", password="", host="", port="")

cities_data = read_json_data(json_file_path)

write_to_postgres(cities_data, conn)

conn.close()