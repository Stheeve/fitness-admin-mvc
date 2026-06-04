import os
import mysql.connector


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "localhost"),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD", "19810203"),
        database=os.getenv("MYSQLDATABASE", "fitness_admin"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )