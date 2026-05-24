import sqlite3
import pandas as pd
import yaml
import os

class SQLExecutor:
    def __init__(self, config_path='config/config.yaml'):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.db_path = self.config['database']['path']
    
    def execute_query(self, query, return_df=True):
        conn = sqlite3.connect(self.db_path)
        if return_df:
            result = pd.read_sql(query, conn)
            conn.close()
            return result
        else:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return None
    
    def execute_sql_file(self, sql_file_path, return_df=True):
        with open(sql_file_path, 'r') as f:
            query = f.read()
        return self.execute_query(query, return_df)
    
    def save_query_result(self, query, output_path):
        result = self.execute_query(query)
        result.to_csv(output_path, index=False)
        print(f"Saved {len(result):,} rows to {output_path}")
        return result
    
    #check everything works well or not 
    def get_table_info(self, table_name):
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_table_sample(self, table_name, n=5):
        query = f"SELECT * FROM {table_name} LIMIT {n}"
        return self.execute_query(query)

if __name__ == "__main__":
    executor = SQLExecutor()
    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = executor.execute_query(tables_query)
    print("Available tables:")
    print(tables) # check all tables are built are not 