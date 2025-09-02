import os
import requests
import numpy as np
from datetime import datetime

def is_valid_finite_number(value):
    """Check if a value is a valid finite number"""
    try:
        if value is None:
            return False

        num_val = float(value)
        return (np.isfinite(num_val) and 
                not np.isnan(num_val) and 
                not np.isinf(num_val) and
                num_val != float('inf') and
                num_val != float('-inf'))
    except (ValueError, TypeError):
        return False

def get_xano_url():
    """Get Xano URL from environment"""
    return os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")

def calculate_total_profit():
    """Calculate total profit from Xano API with strict validation"""
    try:
        xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        response = requests.get(f"{xano_url}/profit", timeout=10)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, list):
            return 0.0

        total = 0.0
        for entry in data:
            if isinstance(entry, dict) and 'amount' in entry:
                amount = entry['amount']
                if is_valid_finite_number(amount):
                    total += float(amount)

        return round(total, 2) if is_valid_finite_number(total) else 0.0
    except Exception:
        return 0.0

def get_profit_by_source():
    """Get profit breakdown by source from Xano API with validation"""
    try:
        xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        response = requests.get(f"{xano_url}/profit", timeout=10)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, list):
            return {}

        source_breakdown = {}
        for entry in data:
            if isinstance(entry, dict) and 'amount' in entry and 'source' in entry:
                amount = entry['amount']
                source = str(entry['source'])

                if is_valid_finite_number(amount):
                    amount_val = float(amount)
                    if source in source_breakdown:
                        source_breakdown[source] += amount_val
                    else:
                        source_breakdown[source] = amount_val

        # Final validation of all values
        return {k: v for k, v in source_breakdown.items() if is_valid_finite_number(v)}
    except Exception:
        return {}

def validate_profit_amount(amount):
    """Validate a profit amount is safe for processing"""
    if amount is None:
        return False

    try:
        amount = float(amount)
        return (np.isfinite(amount) and 
                not np.isnan(amount) and 
                not np.isinf(amount) and
                -999999 <= amount <= 999999)
    except (ValueError, TypeError):
        return False

def calculate_total_profit():
    """Calculate total profit"""
    return 0.0

def get_profit_by_source():
    """Get profit by source"""
    return {}