import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
import math
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calibration import calculateVolatility


def getExpiryDate(expiry_dates: tuple[str]) -> str:
    '''
    Calculates the most suitable expiry date (0.1 years from the present).

    Arguments:
        ticker (Ticker): YAHOO finance ticker object.

    Returns:
        str: Expiry date.
    '''

    expiry_date = expiry_dates[0]
    time_to_expiry = calculateExpiryTime(expiry_time=expiry_date)

    for date in expiry_dates[1:]:
        if abs(calculateExpiryTime(expiry_time=date) - 0.1) < abs(time_to_expiry - 0.1):
            expiry_date = date
            time_to_expiry = calculateExpiryTime(expiry_time=date)


    return expiry_date


def getOptionType() -> str:
    '''
    Gets the user to select an option type (call/put).

    Returns:
        The option type.
    '''
    print("Please select the option type:")
    print("1. Call option\n2. Put Option")

    while True:
        try:
            user_input = int(input("Input: "))
            if user_input == 1:
                return "call"
            elif user_input == 2:
                return "put"
            else:
                raise Exception
        except:
            print("Invalid input.")

def calculateExpiryTime(expiry_time: str) -> float:
    '''
    Calculates the time to expiry in years from the expiry date.

    Arguments:
        expiry_time (str): The expiry date of the option

    Returns:
        The number of years to expiry.
    '''
    expiry_date = dt.strptime(expiry_time, "%Y-%m-%d")
    today = dt.today()
    days_to_expiry = (expiry_date - today).days
    years_to_expiry = days_to_expiry / 365.
    return years_to_expiry

def validateOptionData(option_price: float, stock: float, strike: float, rate: float, time: float, option_type: str) -> bool:
    '''
    Checks if the option is valid (greater than its minimum value)

    Arguments:
        option_price (float): The price of the European option.
        stock (float): The stock asset value.
        strike (float): The strike price of the option.
        rate (float): The risk-free rate.
        time (float): The time to expiry.
    
    Returns:
        True if the option is valid, False otherwise.
    '''
    if option_price < stock - strike * np.exp(-rate * time) and option_type == "call":
        return False
    elif option_price > strike * np.exp(-rate*time) and option_type == "put":
        return False
    elif strike < 0.8 * stock or strike > 1.5 * stock:
        print(f"Option Price: {option_price}\nStock Price: {stock}\nStrike Price: {strike}")
        return False
    elif math.isnan(option_price):
        return False
    else:
        return True

if __name__ == "__main__":

    #Initialises the ticker object that tracks the behaviour of an asset
    finance_symbol = "NVDA"
    ticker = yf.Ticker(ticker=finance_symbol)

    #Initialises the stock value and the risk-free rate
    stock = ticker.info["regularMarketPrice"]
    rate = 0.05

    #Gets the most appropriate expiry date and calculate the expiry time in years
    expiry_date = getExpiryDate(expiry_dates=ticker.options)
    time = calculateExpiryTime(expiry_time=expiry_date)

    #Allows the user to input the option type (call / put)
    option_type = getOptionType()
    if option_type == "call":
        options = ticker.option_chain(expiry_date).calls
    elif option_type == "put":
        options = ticker.option_chain(expiry_date).puts

    #Declares the dictionary of lists that will be used to plot the data
    option_data = {
        "strikes": [],
        "sigmas": [],
        "yf_sigmas": []
    } 


    for index, option in options.iterrows():

        #Calculates the option price (mean of the bid and ask price) and strike price
        option_price = (option["bid"] + option["ask"]) / 2
        strike = option["strike"]

        #Checks if the option is a valid option with a reasonable strike price and obeys arbitrage laws
        if validateOptionData(option_price=option_price, stock=stock, strike=strike, rate=rate, time=time, option_type=option_type):

            #Calculates the volatility using the bisection algorithm
            sigma = calculateVolatility(market_price=option_price, stock=stock, strike=strike, time=time, rate=rate, option_type=option_type)

            #Saves the data into the option_data dictionary to later be plotted
            option_data["strikes"].append(strike)
            option_data["sigmas"].append(sigma)
            option_data["yf_sigmas"].append(option["impliedVolatility"])
    

    figure, axes = plt.subplots(figsize=(10,6))

    #Plots a scatter-line graph of calculated volatility and yahoofinance volatility against strike price
    axes.plot(option_data["strikes"], option_data["sigmas"], "o-", label="Calculated Volatility")
    axes.plot(option_data["strikes"], option_data["yf_sigmas"], "o-", label="Yahoo Volatility")

    #Plots a red vertical line that shows the asset price
    axes.axvline(x=stock, label=rf"Asset Stock: $S=${stock} USD", color="red")

    #Labels the axes and gives the plot a title
    axes.set_title(f"Volatility Smile Plot for {finance_symbol}\nat Expiry {expiry_date}")
    axes.set_xlabel(r"Strike Price, $K$")
    axes.set_ylabel(r"Asset Volatility, $\sigma$")

    #Inserts a textbox clearly showing the time to expiry in years and the risk-free rate as a percentage
    axes.text(x=0.95, y=0.95,
              s=f"Time to Expiry: {time:.2f} years\nRisk-Free Rate: {rate:.2%}",
              transform=axes.transAxes, horizontalalignment="right", verticalalignment="top",
              bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="grey", pad=0.5))

    #Alters the layout of the plot to show the legend and then displays
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

