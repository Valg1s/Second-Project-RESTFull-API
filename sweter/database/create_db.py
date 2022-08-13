from mysql.connector import connect, Error

try:
    with connect(
            host="localhost",
            user="root",
            password="anton2142",
    ) as connection:
        create_db_query = "CREATE DATABASE sport_school"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)

