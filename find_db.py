import mysql.connector
import pandas as pd

def find_database():
    try:
        # Connect without specifying a database first
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin1234",
            port=3306
        )
        cursor = conn.cursor()
        
        # Get all databases
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        target_db = None
        
        print(f"Found databases: {databases}")
        
        for db in databases:
            if db in ['information_schema', 'mysql', 'performance_schema', 'sys']:
                continue
                
            try:
                conn.database = db
                cursor.execute("SHOW TABLES LIKE 'supply_chain'")
                result = cursor.fetchone()
                if result:
                    print(f"Found 'supply_chain' table in database: {db}")
                    target_db = db
                    break
            except Exception as e:
                print(f"Error checking database {db}: {e}")
                
        if target_db:
            # Fetch sample data to check for Product Type
            query = "SELECT * FROM supply_chain LIMIT 5"
            df = pd.read_sql(query, conn)
            print("\nSample Data:")
            print(df.head())
            print("\nColumns:")
            print(df.columns.tolist())
            
            # Check for Product Type candidates
            if 'Product type' not in df.columns:
                print("\n'Product type' column not found. Checking SKU or other columns...")
                print("SKU values:", df['SKU'].unique())
        else:
            print("Could not find 'supply_chain' table in any database.")
            
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    find_database()
