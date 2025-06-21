#  Adam hooker-Brown
#  adhookerbrown@student.rtc.edu
#  6-17-2025
#  CNE370 - Introduction to Virtualization
#  This python script connects to a sharded database and retrieves specific query results from the data.

import mysql.connector

shards = {
    "shard1": {
        "host": "10.10.10.150",
        "port": 4000,
        "user": "maxuser",
        "password": "password",
        "database": "zipcodes_one",
        "table": "zipcodes_one"
    },
    "shard2": {
        "host": "10.10.10.150",
        "port": 4000,
        "user": "maxuser",
        "password": "password",
        "database": "zipcodes_two",
        "table": "zipcodes_two"
    }
}

def yeehaw(header, query, shard_keys=None, filter_empty=False):
    print(f"\n\n\n----- {header} -----")
    results = []

    i = shard_keys if shard_keys else shards.keys()

    for x in i:
        config = shards[x]
        try:
            conn = mysql.connector.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database=config["database"]
            )
            cursor = conn.cursor()
            cursor.execute(query.format(table=config["table"]))
            rows = cursor.fetchall()
            if filter_empty:
                rows = [row for row in rows if row[0] not in (None, '', 'NULL')]
            results.extend(rows)
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error with {x}: {e}")

    if not results:
        print("No results found.")
    else:
        for row in results:
            print(row)

# 1. Largest zipcode from zipcodes_one
yeehaw(
    "1. Largest zipcode in zipcodes_one",
    "SELECT * FROM {table} ORDER BY Zipcode DESC LIMIT 1;",
    shard_keys=["shard1"]
)

# 2. All zipcodes where state = 'KY'
yeehaw(
    "2. All zipcodes where state='KY'",
    "SELECT * FROM {table} WHERE State = 'KY';"
)

# 3. All zipcodes between 40000 and 41000
yeehaw(
    "3. All zipcodes between 40000 and 41000",
    "SELECT * FROM {table} WHERE Zipcode BETWEEN 40000 AND 41000;"
)

# 4. TotalWages where state = 'PA'
yeehaw(
    "4. TotalWages for PA",
    "SELECT TotalWages FROM {table} WHERE State = 'PA';",
    filter_empty=True
)
