import numpy as np
from src.monte_carlo import calculateMonteCarloPrice

def calculateDerivative(random_seed: np.ndarray, option_parameters: dict, parameter_type: str, derivative_type : int=1, step_size: float=1.) -> np.float64:
    '''
    Calculates the derivative (greek) of the European option price with respect to one of the option parameters.

    Arguments:
        random_seed (np.ndarray): The random seed used to calculate the stock value.
        option_parameters (dict): The parameters of the option being calculated (stock, strike, time, rate, volatility and option type).
        parameter_type (str): The option parameter which the option value is differentiated with respect to.
        derivative_type (int): If equal to 1, calculates the first derivative. If equal to 2, calculates the second derivative.
        step_size (float): The increment size used for the finite-difference approximation for the derivative.
    
    Returns:
        (np.float64): The value of the derivative (greek) calculated.
    '''

    #Option parameters when the greek parameters is increased and decreased by the step size
    top_parameters = option_parameters.copy()
    bottom_parameters = option_parameters.copy()
    top_parameters[parameter_type] += step_size
    bottom_parameters[parameter_type] -= step_size

    #Calculates the value of the European option for this increased and decreased value
    top_option_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=top_parameters))
    bottom_option_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=bottom_parameters))

    if derivative_type == 1:
        #Central first-order derivative approximation
        return (top_option_price - bottom_option_price) / (2 * step_size)
    elif derivative_type == 2:
        #Calculates the value of the European option at the default value
        middle_option_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=option_parameters))
        
        #Central second-order derivative approximation
        return (top_option_price - 2*middle_option_price + bottom_option_price) / (step_size ** 2)
    else:
        raise Exception(f"Error: None type returned from calculateDerivative() in calibration.py.\nDerivative type of {derivative_type} does not exist.\nPlease pick either 1 or 2.")