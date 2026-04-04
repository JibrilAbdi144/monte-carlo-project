import numpy as np
import scipy.stats as stats


'''
This subroutine uses the Black-Scholes formula in order to value an call/put option

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
def BlackScholes(option_parameters):

    stock = option_parameters["stock"]
    strike = option_parameters["strike"]
    time = option_parameters["time"]
    rate = option_parameters["rate"]
    sigma = option_parameters["sigma"]
    option_type = option_parameters["option_type"]


    #Calculates the value of d1 and d2
    #for the Black-Scholes formula
    d1 = ((np.log(stock / strike) + (rate + 0.5 * sigma ** 2)) * time) / (sigma * np.sqrt(time))
    d2 = d1 - sigma * np.sqrt(time)

    #Returns the value of a call option if optiontype is "call" or
    #returns the value of a put option if optiontype is "put"
    if option_type == "call":
        call_option = stock * stats.norm.cdf(d1) - strike * np.exp(-rate * time) * stats.norm.cdf(d2)
        return call_option
    elif option_type == "put":
        put_option = strike * np.exp(-rate * time) * stats.norm.cdf(-d2) - stock * stats.norm.cdf(-d1)
        return put_option
    else:
        raise ValueError("Invalid value for 'option type' entered.\nPlease use either 'call' or 'put'.")