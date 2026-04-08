import numpy as np
import math
from monte_carlo import calculateMonteCarloPrice
from tabulate import createRawTable 

def calculateDerivative(random_seed, option_parameters, parameter_type, derivative_type=1, step_size=1.):
    top_parameters = option_parameters.copy()
    bottom_parameters = option_parameters.copy()
    top_parameters[parameter_type] += step_size
    bottom_parameters[parameter_type] -= step_size

    top_option_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=top_parameters))
    bottom_option_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=bottom_parameters))

    if derivative_type == 1:
        return (top_option_price - bottom_option_price) / (2 * step_size)
    elif derivative_type == 2:
        middle_option_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=option_parameters))
        return (top_option_price - 2*middle_option_price + bottom_option_price) / (step_size ** 2)
    else:
        return ValueError(f"Derivative type of {derivative_type} does not exist.\nPlease pick either 1 or 2.")