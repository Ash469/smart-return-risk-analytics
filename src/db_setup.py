import sqlite3
import pandas as pd
import os
import yaml
from pathlib import Path


class DatabaseSetup:
    def __init__(self, config_path='config/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.db_path = self.config['database']['path']
        self.raw_data_path = self.config['paths']['raw_data']

    def create_connection(self):
        conn = sqlite3.connect(self.db_path)
        print(f"Database connection created: {self.db_path}")
        return conn

    def load_csv_to_table(self, conn, csv_filename, table_name):
        csv_path = os.path.join(self.raw_data_path, csv_filename)
        if not os.path.exists(csv_path):
            print(f"File not found: {csv_path}")
            return False
        print(f"Loading {csv_filename}...")
        df = pd.read_csv(csv_path)
        # Load to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Loaded {len(df):,} rows into '{table_name}' table")
        return True

    def setup_database(self):
        print("\n" + "=" * 60)
        print("STARTING DATABASE SETUP")
        print("=" * 60 + "\n")
        conn = self.create_connection()
        csv_table_mapping = {
            'olist_orders_dataset.csv': 'orders',
            'olist_order_items_dataset.csv': 'order_items',
            'olist_customers_dataset.csv': 'customers',
            'olist_order_reviews_dataset.csv': 'reviews',
            'olist_products_dataset.csv': 'products',
        }
        loaded_tables = []
        for csv_file, table_name in csv_table_mapping.items():
            success = self.load_csv_to_table(conn, csv_file, table_name)
            if success:
                loaded_tables.append(table_name)
        print("\n" + "=" * 60)
        print("DATABASE SUMMARY")
        print("=" * 60)
        
        for table in loaded_tables:
            count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0]['count']
            print(f"  {table:20s} : {count:,} rows")

        print("\n" + "=" * 60)
        print("DATABASE SETUP COMPLETE!")
        print("=" * 60 + "\n")
        
        conn.close()
        return loaded_tables


if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.setup_database()