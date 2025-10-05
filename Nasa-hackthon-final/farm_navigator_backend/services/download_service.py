import csv
import json
from io import StringIO
from pathlib import Path

class DownloadService:
    def __init__(self):
        self.data_dir = Path("data")
    
    def prepare_download(self, dataset_id: str, format: str):
        """Prepare dataset for download"""
        # Try to load actual data
        data_file = self.data_dir / f"{dataset_id}.json"
        
        if data_file.exists():
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            # Generate sample data
            data = self._generate_sample_data(dataset_id)
        
        if format == "csv":
            content = self._convert_to_csv(data)
            filename = f"{dataset_id}.csv"
        else:  # json
            content = json.dumps(data, indent=2)
            filename = f"{dataset_id}.json"
        
        return content, filename
    
    def _generate_sample_data(self, dataset_id: str):
        """Generate sample dataset"""
        from datetime import datetime, timedelta
        import random
        
        data = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            row = {
                "date": current_date.strftime("%Y-%m-%d"),
                "value": round(random.uniform(20, 80), 2),
                "latitude": round(random.uniform(-90, 90), 4),
                "longitude": round(random.uniform(-180, 180), 4)
            }
            data.append(row)
        
        return data
    
    def _convert_to_csv(self, data):
        """Convert JSON data to CSV format"""
        if not data:
            return ""
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue()
    
    def prepare_custom_download(self, dataset_id: str, format: str, 
                                start_date=None, end_date=None, variables=None):
        """Prepare customized dataset download with filters"""
        # Load or generate data
        data_file = self.data_dir / f"{dataset_id}.json"
        
        if data_file.exists():
            with open(data_file, 'r') as f:
                data = json.load(f)
        else:
            data = self._generate_sample_data(dataset_id)
        
        # Apply filters (simplified)
        if start_date and end_date:
            data = [d for d in data if start_date <= d.get("date", "") <= end_date]
        
        if variables:
            data = [{k: v for k, v in d.items() if k in variables or k == "date"} for d in data]
        
        if format == "csv":
            content = self._convert_to_csv(data)
            filename = f"{dataset_id}_custom.csv"
        else:
            content = json.dumps(data, indent=2)
            filename = f"{dataset_id}_custom.json"
        
        return content, filename
