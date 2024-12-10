import os
import requests
from semantic_kernel.functions import kernel_function
import datetime
import pyodbc
import difflib

class EngagementsPlugin:
    @kernel_function(name="get_engagements", description="Gets the engagement details for a customer including time room name, and architect.")
    def get_engagements(self, company: str) -> str:
        """
        Retrieves the list of engagements for the week.

        Args:
            company (str): The name of the company or the customer to return engagements details for like their room name.
            
        Returns:
            str: A string describing the engagement.
        """
       
        query = f"""
                    SELECT CustomerName, ResourceName, BookingStartTime
                    FROM (
                        SELECT CustomerName, ResourceName, BookingStartTime,
                            ROW_NUMBER() OVER (PARTITION BY [CustomerName] ORDER BY [BookingStartTime]) AS rn
                        FROM [dbo].[vBookingsView]
                        WHERE MTC LIKE 'Toronto'
                    ) AS subquery
                    WHERE rn = 1
                    AND CustomerName LIKE '%{company}%'
                    AND CAST(BookingStartTime AS DATE) = CAST(GETDATE() AS DATE)
        """

        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv("SQL_SERVER")};DATABASE=RoomDisplay;UID={os.getenv("SQL_USER")};PWD={os.getenv("SQL_PASS")}'

        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            if not result:
                return "I am having trouble finding your room. Please see the receptionist."
            
            room = None
            time = None
            for row in result:
                if (row[0] is not None and row[1] is not None and row[2] is not None):
                    room = row[1]
                    time = row[2]
                    break
                
            if room is None or time is None:
                return "I am having trouble finding your room. Please see the receptionist."
            
        return f"your room is: {room}, have a great session at the Innovation Hub starting at {time}. Enjoy your day!"
