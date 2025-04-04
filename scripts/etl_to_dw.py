import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = pathlib.Path("data").joinpath("dw")
DB_PATH = DW_DIR.joinpath("smart_sales.db")
PREPARED_DATA_DIR = pathlib.Path("data").joinpath("prepared")

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            CustomerID TEXT PRIMARY KEY,
            Name TEXT,
            Region TEXT,
            JoinDate DATE,
            Purchases INTEGER,
            AmountSpent REAL,
            State TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            ProductID TEXT PRIMARY KEY,
            ProductName TEXT,
            Category TEXT,
            UnitPrice REAL,
            QuantityInStock INTEGER,
            Supplier TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            TransactionID TEXT PRIMARY KEY,
            CustomerID TEXT FOREIGN KEY,
            ProductID TEXT FOREIGN KEY,
            SaleDate DATE,
            SaleAmount REAL,
            MemberStatus Text,
            FOREIGN KEY (CustomerID) REFERENCES customer (CustomerID),
            FOREIGN KEY (ProductID) REFERENCES product (ProductID)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    try:
        customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)
    except Exception as e:
        print(f"Error inserting customer data: {e}")

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    try:
        products_df.to_sql("product", cursor.connection, if_exists="append", index=False)
    except Exception as e:
        print(f"Error inserting product data: {e}")
    
def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    try:
        sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)
    except Exception as e:
        print(f"Error inserting sales data: {e}")

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("customers_cleaned.csv"))
        products_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("products_cleaned.csv"))
        sales_df = pd.read_csv(PREPARED_DATA_DIR.joinpath("sales_data_prepared.csv"))

        # Insert data into the database
        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()
