import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_models import validateParameters


'''
Simulates a stock price using a Weiner process and then uses the formula for call/put option to calculate the payoff at the end

Arguments:
S - initial underlying stock price
K - strike price
T - time until expiry
r - risk-free rate (interest)
sigma - volatility of the asset
optiontype - either "call" or "put", used to calculate call options or put options

Returns:
Value of a call option or put option depending on the value of optiontype
'''
def calculateMonteCarloPrice(random_seed, option_parameters):

    validateParameters(option_parameters=option_parameters)

    stock = option_parameters["stock"]
    strike = option_parameters["strike"]
    time = option_parameters["time"]
    rate = option_parameters["rate"]
    sigma = option_parameters["sigma"]
    option_type = option_parameters["option_type"]

    #Simulates the expiry value of a stock underlying asset
    #using a Weiner process (normal distribution)
    drift_term = (rate - 0.5 * sigma ** 2) * time
    diffusion_term = sigma * np.sqrt(time) * random_seed
    final_stock = stock * np.exp(drift_term + diffusion_term)

    #Calculates the payoff of a call/put option
    #using the expiry value of the stock

    #Returns the appropriate payoff value
    #depending on the value of optiontype
    if option_type == "call":
        call_payoff = np.exp(-rate*time)*np.maximum(final_stock - strike, 0)
        return call_payoff
    elif option_type == "put":
        put_payoff = np.exp(-rate*time)*np.maximum(strike - final_stock, 0)
        return put_payoff
    else:
        raise ValueError("Invalid value for 'option type' entered.\nPlease use either 'call' or 'put'.")
    
