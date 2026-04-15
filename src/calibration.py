import yfinance as yf
import numpy as np
from monte_carlo import calculateMonteCarloPrice, generateRandomSeed
from black_scholes import calculateBlackScholesPrice
import matplotlib.pyplot as plt
from datetime import datetime as dt
from src.tabulate import createRawTable

def calibration():
    ticker = yf.Ticker("AAPL")
    closing_price = ticker.info["regularMarketPrice"]
    #print(f"Closing Price: {closing_price}")
    options = ticker.options
    #print(options)
    expiry_date = options[0]
    chain_data = ticker.option_chain(options[0]).calls
    return closing_price, options, chain_data


def calculateExpiryTime(expiry_time):
    expiry_date = dt.strptime(expiry_time, "%Y-%m-%d")
    today = dt.today()
    days_to_expiry = (expiry_date - today).days
    years_to_expiry = days_to_expiry / 365.
    return years_to_expiry


#For European call and put options, Vega is always a positive number.
#This gurantees monotonicity of the V(sigma), allowing the bisection method to be applied
def calculateVolatility(market_price, stock, strike, time, rate, epsilon=0.001, pathway_count=1000000, bounds=(0.001,5.)):
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    solution_found = False
    counter = 0
    minimum_price = stock - strike * np.exp(-rate * time)
    if market_price < minimum_price:
        raise Exception(f"Error: Market price {market_price} < Minimum price {minimum_price}\nArbitrage violation or stale price")
    if market_price > stock:
        raise Exception(f"Error: Market price {market_price} > Asset price {stock}")
    while not solution_found:
        sigma = (lower_bound + upper_bound) / 2
        # monte_carlo_price = np.mean(calculateMonteCarloPrice(random_seed=generateRandomSeed(sample_size=pathway_count, antithetic_variates=True), option_parameters={
        #     "stock": stock,
        #     "strike": strike,
        #     "time": time,
        #     "rate": rate,
        #     "sigma": sigma,
        #     "option_type": "call"
        # }))
        #print(f"Interval: [{lower_bound}, {upper_bound}]")
        black_scholes_price = calculateBlackScholesPrice(option_parameters={
            "stock": stock,
            "strike": strike,
            "time": time,
            "rate": rate,
            "sigma": sigma,
            "option_type": "call"
        })
        if black_scholes_price > market_price:
            upper_bound = sigma
        else:
            lower_bound = sigma
        if abs(black_scholes_price - market_price) < epsilon and upper_bound - lower_bound < epsilon:
            solution_found = True
        if counter > 100000:
            raise Exception(f"Bisection Method took too many iterations.Stock: {stock}\nStrike: {strike}\nOption price: {market_price}\nTime: {time}\nIntermediate Sigma:{sigma}\nIntermediate interval: [{lower_bound}, {upper_bound}]")
        counter += 1
    return sigma


if __name__ == "__main__":

    #expiry_time = "2028-12-15"
    stock, expiry_times, option_chain = calibration()
    main_expiry_time = "2026-05-22"
    time = calculateExpiryTime(expiry_time=main_expiry_time)
    rate = 0.05

    option_data = []
    print(main_expiry_time)
    for index, option in option_chain.iterrows():
        option_price = 0.5 * (option["bid"] + option["ask"])
        strike = option["strike"]
        real_sigma = option["impliedVolatility"]
        if (option_price > 0.05) and (option_price > (stock - strike)) and (strike > stock * 0.8 and strike < stock * 1.8) and option_price > stock - strike * np.exp(-rate * time):
            sigma = calculateVolatility(market_price=option_price, stock=stock, strike=strike, time=time, rate=rate)
            option_data.append({
                "option_price": option_price,
                "strike": strike,
                "real_sigma": real_sigma,
                "sigma": sigma
            })

    createRawTable({
        "Strike": [option["strike"] for option in option_data],
        "Asset Price": [stock] * len(option_data),
        "Option Price": [option["option_price"] for option in option_data],
        "Calculated volatility": [option["sigma"] for option in option_data],
        "Yahoo Volatility": [option["real_sigma"] for option in option_data]
    })

    figure, axes = plt.subplots()
    axes.plot([option["strike"] for option in option_data], [option["sigma"] for option in option_data], label="Calculated Volatility")
    #axes.plot([option["strike"] for option in option_data], [option["real_sigma"] for option in option_data], label="Yahoo Volatility")
    axes.axvline(x=stock, color="red", label="Asset Price")
    plt.legend()
    plt.show()

