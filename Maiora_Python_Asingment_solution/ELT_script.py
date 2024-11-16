import os
import pandas as pd
import sqlite3
import json

def Extract():
    # File paths
    file_path_a = os.path.join('media', 'uploads', 'order_region_a.csv')
    file_path_b = os.path.join('media', 'uploads', 'order_region_b.csv')

    # Ensure files exist
    if not os.path.exists(file_path_a):
        raise FileNotFoundError(f"File not found at: {file_path_a}")
    
    if not os.path.exists(file_path_b):
        raise FileNotFoundError(f"File not found at: {file_path_b}")

    # Read files using pandas
    df_a = pd.read_csv(file_path_a)
    df_b = pd.read_csv(file_path_b)

    # Combine both DataFrames (if needed)
    combined_df = pd.concat([df_a, df_b], ignore_index=True)

    # Transform the data by adding the 'total_sales' column
    transformed_df = transform_data(combined_df)

    # Upload data to the database
    load(transformed_df)  


def transform_data(dataframe):
    # Add the 'total_sales' column: QuantityOrdered * ItemPrice
    dataframe['total_sales'] = dataframe['QuantityOrdered'] * dataframe['ItemPrice']
    
   
    def parse_discount(discount):
        try:
            # Extract the 'Amount' field from the JSON-like string
            discount_data = json.loads(discount.replace("'", '"'))  # Ensure valid JSON format
            return float(discount_data.get('Amount', 0))  # Get Amount, default to 0 if not found
        except Exception as e:
            print(f"Error parsing discount: {e}")
            return 0  

    dataframe['PromotionDiscount'] = dataframe['PromotionDiscount'].apply(parse_discount)
    
    
    dataframe['net_sales'] = dataframe['total_sales'] - dataframe['PromotionDiscount']
    
    
    dataframe = dataframe[dataframe['net_sales'] > 0]
    
    
    dataframe = dataframe.drop_duplicates(subset=['OrderId'])

    
    # print("Transformed DataFrame with 'net_sales':")
    # print(dataframe.head())

    # Return the transformed dataframe
    return dataframe


def load(dataframe, db_name="sales_data.db"):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Ensure the table exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            OrderId TEXT NOT NULL,
            OrderItemId TEXT NOT NULL,
            QuantityOrdered INTEGER NOT NULL,
            ItemPrice REAL NOT NULL,
            PromotionDiscount TEXT,
            TotalSales FLOAT NOT NULL,
            NetSales FLOAT NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        for index, row in dataframe.iterrows():
            insert_query = """
            INSERT INTO orders (OrderId, OrderItemId, QuantityOrdered, ItemPrice, PromotionDiscount, TotalSales, NetSales)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, (
                row['OrderId'],
                row['OrderItemId'],
                row['QuantityOrdered'],
                row['ItemPrice'],
                row['PromotionDiscount'],
                row['total_sales'],
                row['net_sales']  
            ))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("Data uploaded successfully to the database.")

    except sqlite3.Error as e:
        print(f"An error occurred while uploading data to the database: {e}")


if __name__ == "__main__":
    Extract()


        




    
    

    