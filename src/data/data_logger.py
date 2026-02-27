"""
Data Logging Module
Records plant measurements and health data to CSV
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, List


class DataLogger:
    """
    Log plant health data to CSV file
    """
    
    def __init__(self, log_file: str = "data/plant_records.csv"):
        """
        Initialize data logger
        
        Args:
            log_file: Path to CSV log file
        """
        self.log_file = log_file
        self.columns = [
            'timestamp',
            'plant_id',
            'group',
            'leaf_area',
            'green_intensity',
            'green_index',
            'plant_height',
            'plant_width',
            'compactness',
            'growth_rate',
            'health_status',
            'confidence'
        ]
        
        # Create file with headers if doesn't exist
        if not os.path.exists(log_file):
            self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Create empty log file with headers"""
        df = pd.DataFrame(columns=self.columns)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        df.to_csv(self.log_file, index=False)
        print(f"Initialized log file: {self.log_file}")
    
    def log_measurement(self, data: Dict):
        """
        Log a single measurement
        
        Args:
            data: Dictionary containing measurement data
        """
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create DataFrame from single record
        df_new = pd.DataFrame([data])
        
        # Append to CSV
        if os.path.exists(self.log_file):
            df_new.to_csv(self.log_file, mode='a', header=False, index=False)
        else:
            df_new.to_csv(self.log_file, mode='w', header=True, index=False)
        
        print(f"✅ Logged measurement for Plant {data.get('plant_id', 'unknown')}")
    
    def log_batch(self, data_list: List[Dict]):
        """
        Log multiple measurements at once
        
        Args:
            data_list: List of measurement dictionaries
        """
        # Add timestamps
        for data in data_list:
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create DataFrame
        df_new = pd.DataFrame(data_list)
        
        # Append to CSV
        if os.path.exists(self.log_file):
            df_new.to_csv(self.log_file, mode='a', header=False, index=False)
        else:
            df_new.to_csv(self.log_file, mode='w', header=True, index=False)
        
        print(f"✅ Logged {len(data_list)} measurements")
    
    def load_history(self) -> pd.DataFrame:
        """
        Load complete measurement history
        
        Returns:
            DataFrame with all historical data
        """
        if not os.path.exists(self.log_file):
            print(f"No history found at {self.log_file}")
            return pd.DataFrame(columns=self.columns)
        
        df = pd.read_csv(self.log_file)
        return df
    
    def get_plant_history(self, plant_id: str) -> pd.DataFrame:
        """
        Get history for specific plant
        
        Args:
            plant_id: Plant identifier
            
        Returns:
            DataFrame with plant's history
        """
        df = self.load_history()
        if df.empty:
            return df
        
        plant_data = df[df['plant_id'] == plant_id]
        return plant_data.sort_values('timestamp')
    
    def get_group_history(self, group: str) -> pd.DataFrame:
        """
        Get history for specific group
        
        Args:
            group: Group name
            
        Returns:
            DataFrame with group's history
        """
        df = self.load_history()
        if df.empty:
            return df
        
        group_data = df[df['group'] == group]
        return group_data.sort_values('timestamp')
    
    def get_latest_measurement(self, plant_id: str) -> Dict:
        """
        Get most recent measurement for plant
        
        Args:
            plant_id: Plant identifier
            
        Returns:
            Dictionary with latest measurement
        """
        plant_hist = self.get_plant_history(plant_id)
        
        if plant_hist.empty:
            return {}
        
        latest = plant_hist.iloc[-1].to_dict()
        return latest
    
    def get_statistics(self) -> Dict:
        """
        Get summary statistics from log
        
        Returns:
            Dictionary with statistics
        """
        df = self.load_history()
        
        if df.empty:
            return {
                'total_records': 0,
                'unique_plants': 0,
                'groups': []
            }
        
        stats = {
            'total_records': len(df),
            'unique_plants': df['plant_id'].nunique() if 'plant_id' in df.columns else 0,
            'groups': df['group'].unique().tolist() if 'group' in df.columns else [],
            'date_range': {
                'start': df['timestamp'].min() if 'timestamp' in df.columns else None,
                'end': df['timestamp'].max() if 'timestamp' in df.columns else None
            }
        }
        
        return stats


def log_data(data: Dict, log_file: str = "data/plant_records.csv"):
    """
    Convenience function to log data
    
    Args:
        data: Measurement data
        log_file: Path to log file
    """
    logger = DataLogger(log_file)
    logger.log_measurement(data)


if __name__ == "__main__":
    print("Data Logging Module")
    print("=" * 50)
    
    # Example usage
    logger = DataLogger()
    
    # Get statistics
    stats = logger.get_statistics()
    print(f"\nLog Statistics:")
    print(f"  Total Records: {stats['total_records']}")
    print(f"  Unique Plants: {stats['unique_plants']}")
    print(f"  Groups: {stats['groups']}")
