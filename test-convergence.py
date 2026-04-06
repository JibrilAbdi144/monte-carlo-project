import numpy as np
import matplotlib.pyplot as plt
import math
from monte_carlo import calculateMonteCarloPrice
from black_scholes import calculateBlackScholesPrice

def generateRandomSeeds(pathway_count):
    return np.array([np.random.normal()] * pathway_count)

def generateMonteCarloPrices(pathway_count, option_parameters):
    monte_carlo_prices = np.array([
        calculateMonteCarloPrice(random_seed=np.random.normal(), option_parameters=option_parameters) for x in range(pathway_count)
    ])
    return monte_carlo_prices

def calculateMeanMonteCarloPrice(pathway_count, option_parameters):
    monte_carlo_prices = np.array([
        calculateMonteCarloPrice(random_seed=np.random.normal(),option_parameters=option_parameters) for x in range(pathway_count)
    ])
    return np.mean(monte_carlo_prices)

def calculatePriceAbsoluteError(pathway_count, option_parameters):

    monte_carlo_price = calculateMeanMonteCarloPrice(pathway_count=pathway_count, option_parameters=option_parameters)
    black_scholes_price = calculateBlackScholesPrice(option_parameters=option_parameters)

    absolute_error = np.abs(monte_carlo_price - black_scholes_price)

    return absolute_error

def generateTablePriceData(pathway_counts, option_parameters):
    table_columns = ["Pathway Count", "Mean of Monte Carlo Prices", "Black Scholes Price", "Absolute Error", "Percentage Error"]

    table_data = []
    black_scholes_price = float(calculateBlackScholesPrice(option_parameters=option_parameters))
    for pathway_count in pathway_counts:
        monte_carlo_prices = generateMonteCarloPrices(pathway_count=pathway_count, option_parameters=option_parameters)
        mean_monte_carlo_price = float(np.mean(monte_carlo_prices))
        absolute_error = abs(mean_monte_carlo_price - black_scholes_price)
        percentage_error = 100 * absolute_error / black_scholes_price
        table_data.append([
            pathway_count,
            mean_monte_carlo_price,
            black_scholes_price,
            absolute_error,
            percentage_error
        ])

    return table_columns, table_data
    

def tabulatePriceData(pathway_counts, option_parameters):

    column_width = 30
    table_columns, table_data = generateTablePriceData(pathway_counts=pathway_counts, option_parameters=option_parameters)

    print("|" + "|".join([f"{table_column:^{column_width}}" for table_column in table_columns]) + "|")
    print("|:" + ":|:".join(["-"*(column_width - 2) for column in table_columns]) + ":|")
    for row in table_data:
        print("|" + "|".join([
            f"{item:^{column_width}}" if index == 0 else f"{item:^{column_width}.2f}" for index, item in enumerate(row)
        ]) + "|")

def getBestFitLine(pathway_counts, relative_errors):

    log_pathway_counts = np.log(pathway_counts)
    log_relative_errors = np.log(relative_errors)

    a, b = np.polyfit(log_pathway_counts, log_relative_errors, 1)
    R = np.corrcoef(log_pathway_counts, log_relative_errors)[0,1]

    return a, b, R

def plotPriceConvergence(pathway_counts, option_parameters):
    monte_carlo_prices = np.array([
        np.median([
            np.mean(generateMonteCarloPrices(pathway_count=pathway_count, option_parameters=option_parameters)) for i in range(3)
        ]) for pathway_count in pathway_counts
    ])
    black_scholes_price = calculateBlackScholesPrice(option_parameters=option_parameters)
    relative_errors = np.abs(monte_carlo_prices - black_scholes_price) / black_scholes_price

    a, b, R = getBestFitLine(pathway_counts, relative_errors)
    print(a, b, R)

    figure, axes = plt.subplots()
    axes.loglog(pathway_counts, relative_errors, "o")
    axes.plot(pathway_counts, [a * pathway_count + b for pathway_count in pathway_counts], "-")
    plt.show()
    


if __name__ == "__main__":

    pathway_counts = [100 * math.floor(2 ** n) for n in range(8)]
    option_parameters = {
        "stock": 100,
        "strike": 100,
        "time": 1,
        "rate": 0.05,
        "sigma": 0.2,
        "option_type": "call"
    }

    #tabulatePriceData(pathway_counts=pathway_counts, option_parameters=option_parameters)
    plotPriceConvergence(pathway_counts=pathway_counts, option_parameters=option_parameters)
