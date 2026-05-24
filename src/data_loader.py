import pandas as pd
import os
from sql_executor import SQLExecutor
from utils import print_section_header, save_df_to_csv

class DataLoader:
    def __init__(self):
        self.executor = SQLExecutor()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sql_dir = os.path.join(base_dir, 'sql')
        self.output_dir = os.path.join(base_dir, 'data', 'sql_outputs')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def execute_sql_file(self, sql_filename, output_filename=None):
        sql_path = os.path.join(self.sql_dir, sql_filename)
        print(f"\n Executing: {sql_filename}")
        with open(sql_path, 'r') as f:
            query = f.read()
        statements = [s.strip() for s in query.split(';') if s.strip()]
        if len(statements) > 1:
            results = []
            for i, stmt in enumerate(statements):
                try:
                    df = self.executor.execute_query(stmt)
                    results.append(df)
                except Exception as e:
                    print(f"Warning on statement {i+1}: {e}")
            result = pd.concat(results, ignore_index=True) if results else pd.DataFrame()
        else:
            result = self.executor.execute_query(statements[0]) 
        print(f"Query executed: {len(result):,} rows returned")
        
        if output_filename:
            output_path = os.path.join(self.output_dir, output_filename)
            save_df_to_csv(result, output_path, name=output_filename)
        return result
    
    def run_all_feature_queries(self):
        print_section_header("RUNNING ALL FEATURE ENGINEERING QUERIES")

        print("\n Step 1: Data Quality Checks")
        quality_results = self.execute_sql_file(
            '02_data_quality_checks.sql',
            'data_quality_report.csv'
        )
    
        print("\n Step 2: Customer Features")
        customer_features = self.execute_sql_file(
            '03_customer_features.sql',
            'customer_features.csv'
        )
        print(f"Generated features for {len(customer_features):,} customers")
        
        print("\n Step 3: Product Features")
        product_features = self.execute_sql_file(
            '04_product_features.sql',
            'product_features.csv'
        )
        print(f"Generated features for {len(product_features):,} products")
        
        print("\n Step 4: Order-Level Features (with simulated returns)")
        #most important file till now as it contain return flag
        order_features = self.execute_sql_file(
            '05_order_level_features.sql',
            'order_features_with_returns.csv'
        )
        print(f"Generated features for {len(order_features):,} orders")
        
        # Show return distribution
        return_dist = order_features['is_returned'].value_counts()
        return_rate = (return_dist.get(1, 0) / len(order_features)) * 100
        print(f"\nReturn Distribution:")    # let's see how many orders are returned and how many are not 
        print(f"- Not Returned: {return_dist.get(0, 0):,} ({100-return_rate:.1f}%)")  
        print(f"- Returned: {return_dist.get(1, 0):,} ({return_rate:.1f}%)")   
        
        print("\n" + "="*60)
        print("ALL FEATURE QUERIES EXECUTED SUCCESSFULLY!")
        print("="*60)
        print(f"\nOutput files saved to: {self.output_dir}/")
        
        return {
            'customer_features': customer_features,
            'product_features': product_features,
            'order_features': order_features
        }

if __name__ == "__main__":
    loader = DataLoader()
    results = loader.run_all_feature_queries()
    print("\nData loading complete!")
