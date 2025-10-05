from pathlib import Path

def get_data_path(filename: str) -> Path:
    """Get full path to data file"""
    return Path("data") / filename

def validate_date_format(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD)"""
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False