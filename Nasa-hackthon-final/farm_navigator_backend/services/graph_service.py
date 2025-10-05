import json
from pathlib import Path
from datetime import datetime, timedelta
import random

class GraphService:
    def __init__(self):
        self.data_dir = Path("data")
    
    def get_graph_data(self, dataset_id: str):
        """Get graph data for a dataset"""
        # Try to load from file first
        graph_file = self.data_dir / f"{dataset_id}_graph.json"
        if graph_file.exists():
            with open(graph_file, 'r') as f:
                return json.load(f)
        
        # Generate sample data if file doesn't exist
        return self._generate_sample_graph(dataset_id)
    
    def _generate_sample_graph(self, dataset_id: str):
        """Generate sample graph data"""
        # Generate 30 days of data
        labels = []
        values = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            current_date = base_date + timedelta(days=i)
            labels.append(current_date.strftime("%Y-%m-%d"))
            # Generate sample values based on dataset type
            if "moisture" in dataset_id or "precipitation" in dataset_id:
                values.append(round(random.uniform(20, 80), 2))
            elif "temperature" in dataset_id:
                values.append(round(random.uniform(15, 35), 2))
            elif "ndvi" in dataset_id:
                values.append(round(random.uniform(0.2, 0.9), 3))
            else:
                values.append(round(random.uniform(0, 100), 2))
        
        return {
            "dataset_id": dataset_id,
            "chart_type": "line",
            "labels": labels,
            "datasets": [
                {
                    "label": dataset_id.replace("_", " ").title(),
                    "data": values,
                    "borderColor": "#34d399",
                    "backgroundColor": "rgba(52, 211, 153, 0.1)"
                }
            ]
        }
    
    def get_filtered_graph_data(self, dataset_id: str, start_date=None, end_date=None, location=None):
        """Get filtered graph data"""
        base_data = self.get_graph_data(dataset_id)
        # Apply filters (simplified implementation)
        # In production, you would filter actual data based on parameters
        return base_data