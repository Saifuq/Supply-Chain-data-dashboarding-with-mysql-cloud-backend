import mysql.connector
import pandas as pd

def export_to_csv():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin1234",
            port=3306,
            database="startersql"
        )
        
        query = "SELECT * FROM supply_chain"
        df = pd.read_sql(query, conn)
        
        # Save to CSV
        df.to_csv("supply_chain_data.csv", index=False)
        print("Successfully exported 'supply_chain' table to 'supply_chain_data.csv'")
        print(f"Rows exported: {len(df)}")
        
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    export_to_csv()
