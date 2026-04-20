import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.black_scholes import calculateBlackScholesPrice
from src.monte_carlo import calculateMonteCarloPrice, generateRandomSeed
import numpy as np

def testOptionPrice():
    '''
    Tests Monte-Carlo & Black-Scholes option price with the following parameters:
    stock = 100, strike = 100, time = 1.0, rate = 0.05, sigma = 0.2, option_type = "call", pathway_count=10,000,000 (monte-carlo only)
    -> option price ~ 10.451
    '''

    option_parameters = {
        "stock": 100,
        "strike": 100,
        "time": 1.0,
        "rate": 0.05,
        "sigma": 0.2,
        "option_type": "call"
    }

    #Calculating the option price
    black_scholes_price = calculateBlackScholesPrice(option_parameters=option_parameters)
    pathway_count = 100000000
    monte_carlo_price = np.mean(calculateMonteCarloPrice(
        random_seed=np.random.normal(size=pathway_count),
        option_parameters=option_parameters
    ))
    expected_price = 10.451
    
    #The option price for both methods should have an absolute error of less than epsilon to be a success
    epsilon = 0.01
    assert abs(black_scholes_price - expected_price) < epsilon and abs(monte_carlo_price - expected_price) < epsilon, f"Expected: {expected_price},\nMonte-Carlo: {monte_carlo_price},\nBlack-Scholes: {black_scholes_price}"


def testPutCallParity():
    '''
    Tests Monte-Carlo and Black-Scholes Put-Call Parity C - P = S - Kexp(-rT) with known parameters:
    stock = 100, strike = 100, time = 1.0, rate = 0.05, sigma = 0.2, option_type = "call", pathway_count=10,000,000 (monte-carlo only)
    '''

    stock = 100
    strike = 100
    time = 1.0
    rate = 0.05
    sigma = 0.2


    #Calculating call and put option values for both black-scholes and monte-carlo methods
    black_scholes_call = calculateBlackScholesPrice({"stock": stock, "strike": strike, "time": time, "rate": rate, "sigma": sigma, "option_type": "call"})
    black_scholes_put = calculateBlackScholesPrice({"stock": stock, "strike": strike, "time": time, "rate": rate, "sigma": sigma, "option_type": "put"})

    pathway_count = 10000000
    random_seed = generateRandomSeed(sample_size=pathway_count, antithetic_variates=True)
    monte_carlo_call = np.mean(calculateMonteCarloPrice(
        random_seed = random_seed,
        option_parameters={"stock": stock, "strike": strike, "time": time, "rate": rate, "sigma": sigma, "option_type": "call"}
    ))
    monte_carlo_put = np.mean(calculateMonteCarloPrice(
        random_seed = random_seed,
        option_parameters={"stock": stock, "strike": strike, "time": time, "rate": rate, "sigma": sigma, "option_type": "put"}
    ))

    #Calculating the option parity
    option_parity = stock - strike * np.exp(-rate * time)

    #Black-scholes and monte-carlo option parity must both have an absolute error of less than epsilon to be successful
    epsilon = 0.01
    black_scholes_test = abs((black_scholes_call - black_scholes_put) - option_parity) < epsilon
    monte_carlo_test = abs((monte_carlo_call - monte_carlo_put) - option_parity) < epsilon

    assert black_scholes_test and monte_carlo_test