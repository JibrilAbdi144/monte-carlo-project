import yfinance as yf
import numpy as np
from src.black_scholes import calculateBlackScholesPrice
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
    chain_data = ticker.option_chain("2026-05-22").calls
    return closing_price, options, chain_data


def calculateExpiryTime(expiry_time):
    expiry_date = dt.strptime(expiry_time, "%Y-%m-%d")
    today = dt.today()
    days_to_expiry = (expiry_date - today).days
    years_to_expiry = days_to_expiry / 365.
    return years_to_expiry


#For European call and put options, Vega is always a positive number.
#This guarantees monotonicity of the V(sigma), allowing the bisection method to be applied
def calculateVolatility(market_price: float, stock: float, strike: float, time: float, rate: float, option_type: str="call", epsilon: float=0.001, bounds: tuple[float, float]=(0.001, 5.)) -> float:
    '''
    Implements the bisection method algorithm to calculate the implied volatility.

    Arguments:
        market_price (float): The price of the European option.
        stock (float): The value of the stock asset.
        strike (float): The strike price of the option.
        time (float): The time to expiry in years. (Ideally around 0.1).
        rate (float): The risk-free rate of the market.
        option_type (str, optional): The type of the option (call or put), the default is call.
        epsilon (float, optional): The tolerance method for the bisection method solver.
        bounds (tuple[float, float], optional): The starting interval of the bisection method.

    Returns:
        sigma (float): The implied volatility of the stock asset.
    '''
    lower_bound = bounds[0]
    upper_bound = bounds[1]
    solution_found = False
    counter = 0
    
    if option_type == "call":
        minimum_price = stock - strike * np.exp(-rate * time)
        if market_price < minimum_price:
            raise Exception(f"Error: Market price {market_price} < Minimum price {minimum_price}\nArbitrage violation or stale price")
    elif option_type == "put":
        maximum_price = strike * np.exp(-rate * time)
        if market_price > maximum_price:
            raise Exception(f"Error: Market price {market_price} > Maximum price {maximum_price}\nArbitrage violation or stale price")
    if market_price > stock:
        raise Exception(f"Error: Market price {market_price} > Asset price {stock}")
    while not solution_found:
        sigma = (lower_bound + upper_bound) / 2
        black_scholes_price = calculateBlackScholesPrice(option_parameters={
            "stock": stock,
            "strike": strike,
            "time": time,
            "rate": rate,
            "sigma": sigma,
            "option_type": option_type
        })
        if black_scholes_price > market_price:
            upper_bound = sigma
        else:
            lower_bound = sigma
        if abs(black_scholes_price - market_price) < epsilon:
            solution_found = True
        if counter > 100000:
            raise Exception(f"Bisection Method took too many iterations.\nStock: {stock}\nStrike: {strike}\nOption price: {market_price}\nTime: {time}\nIntermediate Sigma:{sigma}\nIntermediate interval: [{lower_bound}, {upper_bound}]")
        counter += 1
    return sigma
