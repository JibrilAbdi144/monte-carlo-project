import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calibration import calculateVolatility
from src.black_scholes import calculateBlackScholesPrice

def testCalibration():
    '''
    Tests the bisection method algorithm for finding volatility (sigma) from a known option price using the following parameters:
    stock = 100, strike = 100, time = 1.0, rate = 0.05, sigma = 0.2, option_type = "call"
    -> option_price ~ 10.451
    '''
    option_parameters = {
        "stock": 100,
        "strike": 100,
        "time": 1.0,
        "rate": 0.05,
        "sigma": 0.2,
        "option_type": "call"
    }

    #Calculating the option price from the above given parameters
    option_price = calculateBlackScholesPrice(option_parameters=option_parameters)

    #Calculating sigma (backwards problem) using the option price
    calculated_sigma = calculateVolatility(
        market_price=option_price,
        stock=option_parameters["stock"],
        strike=option_parameters["strike"],
        time=option_parameters["time"],
        rate=option_parameters["rate"],
        option_type=option_parameters["option_type"]
    )

    #Absolute error of calculated sigma must be less than epsilon for success
    epsilon = 0.01
    assert abs(calculated_sigma - option_parameters["sigma"]) < epsilon, f"Expected Sigma: {option_parameters["sigma"]}\nCalculated Sigma: {calculated_sigma}"