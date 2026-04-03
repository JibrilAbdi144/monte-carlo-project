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
def BlackScholes(S, K, T, r, sigma, optiontype):
    #Calculates the value of d1 and d2
    #for the Black-Scholes formula
    d1 = ((np.log(S/K) + (r+0.5*sigma**2)) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    #Returns the value of a call option if optiontype is "call" or
    #returns the value of a put option if optiontype is "put"
    if optiontype == "call":
        call_option = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
        return call_option
    elif optiontype == "put":
        put_option = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
        return put_option
    else:
        raise ValueError("Invalid value for 'option type' entered.\nPlease use either 'call' or 'put'.")