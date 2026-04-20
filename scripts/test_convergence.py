#Importing necessary modules
import numpy as np
import math
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.black_scholes import calculateBlackScholesPrice
from src.monte_carlo import calculateMonteCarloPrice, generateRandomSeed
from src.plot_convergence import plotConvergenceGraph
from src.tabulate import createRawTable
from src.data_models import validateParameters  

if __name__ == "__main__":


    #List of simulation pathways to be analysed
    #(e.g. [1000, 2000, 4000, 8000, 16 000, 32 000, 64 000, 128 000])
    pathway_counts = [math.floor(100 * 2 ** n) for n in np.linspace(1., 16., 16)]

    #Defining the European option parameters
    option_parameters = {
        "stock": 100,
        "strike": 100,
        "time": 1,
        "rate": 0.05,
        "sigma": 0.2,
        "option_type": "call"
    }

    #Calculating the option prices by Monte-Carlo method and Black-Scholes method
    mean_monte_carlo_prices = [np.mean(calculateMonteCarloPrice(
        random_seed=generateRandomSeed(sample_size=pathway_count, antithetic_variates=False),
        option_parameters=option_parameters
    )) for pathway_count in pathway_counts]
    black_scholes_price = calculateBlackScholesPrice(option_parameters=option_parameters)

    #Calculating their absolute errors and percentage errors
    absolute_errors = [abs(mean_monte_carlo_price - black_scholes_price) for mean_monte_carlo_price in mean_monte_carlo_prices]
    relative_errors = [absolute_error / black_scholes_price for absolute_error in absolute_errors]

    #Displaying the convergence data in a raw terminal table
    createRawTable({
        "pathway count": pathway_counts,
        "black-scholes price": [black_scholes_price] * len(pathway_counts),
        "arithmetic mean": mean_monte_carlo_prices,
        "absolute error": absolute_errors,
        "percentage error": relative_errors * 100
    })

    #Plotting the converging data using a matplotlib figure
    plotConvergenceGraph(pathway_counts=pathway_counts, relative_errors=relative_errors)
