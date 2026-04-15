import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_models import validateParameters

def calculateMonteCarloPrice(random_seed: np.ndarray, option_parameters: dict, return_stock:bool=False) -> np.ndarray:
    '''
    Calculates the values of the stock at the time of expiry, and then calculates the pay-off.

    Arguments:
        random_seed (np.ndarray): The random seed used to calculate the stock value.
        option_parameters (dict): The parameters of the option being calculated (stock, strike, time, rate, volatility and option type).
        return_stock (bool, optional): If False, returns the value of the option contract. If True, returns the stock prices at the time of expiry. False by default.

    Returns:
        Value of a call option or put option depending on the value of optiontype
    '''

    #Validates the option parameters to make sure they are safe for calculation
    validateParameters(option_parameters=option_parameters)

    #Initialises the variables used for calculation
    stock = option_parameters["stock"]
    strike = option_parameters["strike"]
    time = option_parameters["time"]
    rate = option_parameters["rate"]
    sigma = option_parameters["sigma"]
    option_type = option_parameters["option_type"]

    #Calculates the stock price at the time of expiry
    drift_term = (rate - 0.5 * sigma ** 2) * time
    diffusion_term = sigma * np.sqrt(time) * random_seed
    final_stock = stock * np.exp(drift_term + diffusion_term)

    #Returns the value of the stock price at the time of expiry if return_stock is True
    if return_stock:
        return final_stock
    else:
        #Returns the value of the European option (whether it is call or put) if return_stock is False
        if option_type == "call":
            call_payoff = np.exp(-rate*time)*np.maximum(final_stock - strike, 0)
            return call_payoff
        elif option_type == "put":
            put_payoff = np.exp(-rate*time)*np.maximum(strike - final_stock, 0)
            return put_payoff
        raise Exception("Error: None type returned from calculateMonteCarloPrice in src/monte_carlo.py.")
        

def generateRandomSeed(sample_size: int, antithetic_variates=False) -> np.ndarray:
    '''
    Generates a random seed by simulating random walks.

    Arguments:
        sample_size (int): The size of the random seed.
        antithetic_variates (bool, optional): If True, generates a random seed using antithetic variates. If False, generates a standard independent random seed.

    Returns:
        (np.ndarray): The random seed.

    '''
    if antithetic_variates:
        #Calculates the random seed using antithetic variates
        random_seed = np.random.normal(size=(sample_size + 1) // 2)
        return np.concatenate((random_seed, -random_seed))
    else:
        #Calculates the random seed using independent random variables
        random_seed = np.random.normal(size=sample_size)
        return random_seed
    
