import os
import requests
from semantic_kernel.functions import kernel_function
import datetime
import pyodbc
import difflib
import json

class EngagementsPlugin:
    @kernel_function(name="get_engagements", description="""
                                                                Retrieves the list of engagements for the day to be passed on to the next function (find the person's room by company)
                                                                run this functionto get this list of rooms if the customer asks to guide them or they are lost.
                                                         """
                    )
    def get_engagements(self) -> str:
        """
            Retrieves the list of engagements for the day to be passed on to the next function (find the person's room by company)
            run this functionto get this list of rooms if the customer asks to guide them or they are lost.
           
        Returns:
            str: A JSON Array of engagements for the day including room Information.
            
        """
       
        query = f"""
              SELECT CustomerName, ResourceName, BookingStartTime, rt
                FROM [dbo].[vBookingsView-with_RType]
                WHERE MTC LIKE 'Toronto' 
                    AND CAST(BookingStartTime AS DATE) = CAST(GETDATE() AS DATE) and
                    rt = 'Room'
        """

        result = self.run_sql_query(
            server=os.getenv("SQL_SERVER"),
            database="RoomDisplay",
            username=os.getenv("SQL_USER"),
            password=os.getenv("SQL_PASS"),
            query=query
        )

        if not result:
            return "I am having trouble getting a list of engagements for today. Please see the receptionist."
                            
        print(result)
        return result

    def run_sql_query(self, server: str, database: str, username: str, password: str, query: str):
        """
        Runs a SQL query against the specified SQL database using SQL authentication.

        Args:
            server (str): The SQL server address.
            database (str): The name of the database.
            username (str): The SQL username.
            password (str): The SQL password.
            query (str): The SQL query to execute.

        Returns:
            str: The JSON serialized result of the query.
        """
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            for row in result:
                for key, value in row.items():
                    if isinstance(value, datetime.datetime):
                        row[key] = value.isoformat()
        return json.dumps(result)
