import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_models import validateParameters

option_parameters = {
    "stock": 100,
    "strike": 100,
    "time": 1,
    "rate": 0.05,
    "sigma": 0.2,
    "option_type": "call"
}

try:
    validateParameters(option_parameters=option_parameters)
    print("Test complete: Valid input accepted")
except Exception as error:
    print(f"Test complete: {error}")