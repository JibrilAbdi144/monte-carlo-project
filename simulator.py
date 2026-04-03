import numpy as np

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
def OptionSimulator(stock, strike, time, rate, sigma, optiontype):

    #Simulates the expiry value of a stock underlying asset
    #using a Weiner process (normal distribution)
    drift_term = (rate - 0.5 * sigma ** 2) * time
    diffusion_term = sigma * np.sqrt(time) * np.random.normal()
    final_stock = stock * np.exp(drift_term + diffusion_term)

    #Calculates the payoff of a call/put option
    #using the expiry value of the stock
    call_payoff = np.exp(-rate*time)*max(final_stock - strike, 0)
    put_payoff = np.exp(-rate*time)*max(strike - final_stock, 0)

    #Returns the appropriate payoff value
    #depending on the value of optiontype
    if optiontype == "call":
        return call_payoff
    elif optiontype == "put":
        return put_payoff
    else:
        raise ValueError("Invalid value for 'option type' entered.\nPlease use either 'call' or 'put'.")
    
