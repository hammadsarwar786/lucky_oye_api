# database.py
import psycopg2
from fastapi import HTTPException

# Replace these values with your actual database credentials
hostname = 'ec2-52-0-41-103.compute-1.amazonaws.com'
# hostname = "0.0.0.0"
database_name = 'crmdb'
username = 'postgres'
password = 'Admin@12345'

def get_database_connection():
    try:
        connection = psycopg2.connect(
            host=hostname,
            database=database_name,
            user=username,
            password=password
        )
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Connection Error: {str(e)}")

# for login
def fetch_single_row(query, params=None):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        if params is not None:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        return row
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query Execution Error: {str(e)}")

# for registration
def register_user(query, params):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

        return {"success": True, "message": "User Has Been Registered Successfully!"}
    except psycopg2.Error as e:
        error_message = f"Query Execution Error: {e}"
        print(error_message)  # Print the error message for debugging
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"Other Error: {e}"
        print(error_message)  # Print the error message for debugging
        raise HTTPException(status_code=500, detail=error_message)




# def execute_query(query, params=None):
#     try:
#         connection = get_database_connection()
#         cursor = connection.cursor()
#
#         if params is not None:
#             cursor.execute(query, params)
#         else:
#             cursor.execute(query)
#
#         rows = cursor.fetchall()
#
#         cursor.close()
#         connection.close()
#
#         return rows
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Query Execution Error: {str(e)}")