import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.greeks import calculateDerivative
from src.monte_carlo import generateRandomSeed

def testGreeks():
    '''
    Tests Monte-Carlo derived greeks against known values with the following parameters:
    stock = 100, strike = 100, time = 1.0, rate = 0.05, sigma = 0.2, option_type = "call", pathwaycount = 10,000,000
    -> Delta ~ 0.6368, Gamma ~ 0.01876, Vega ~ 37.52, Theta ~ 6.41, Rho ~ 53.23
    '''

    #Generates random seed
    pathway_count = 10000000
    random_seed = generateRandomSeed(sample_size=pathway_count, antithetic_variates=True)

    #Initalises option parameters
    option_parameters = {
        "stock": 100,
        "strike": 100,
        "time": 1.0,
        "rate": 0.05,
        "sigma": 0.2,
        "option_type": "call"
    }

    #Calculating the greeks using a monte-carlo simulation
    calculated_delta = calculateDerivative(
        random_seed=random_seed,
        option_parameters=option_parameters,
        parameter_type="stock"
    )
    calculated_gamma = calculateDerivative(
        random_seed=random_seed,
        option_parameters=option_parameters,
        parameter_type="stock",
        derivative_type=2
    )
    calculated_vega = calculateDerivative(
        random_seed=random_seed,
        option_parameters=option_parameters,
        parameter_type="sigma",
        step_size=0.002
    )
    calculated_theta = calculateDerivative(
        random_seed=random_seed,
        option_parameters=option_parameters,
        parameter_type="time",
        step_size=0.01
    )
    calculated_rho = calculateDerivative(
        random_seed=random_seed,
        option_parameters=option_parameters,
        parameter_type="rate",
        step_size=0.0005
    )

    #Known values of greeks
    expected_delta = 0.6368
    expected_gamma = 0.01876
    expected_vega = 37.52
    expected_theta = 6.41
    expected_rho = 53.23

    epsilon = 1.
    #Absolute error of greeks must be within epsilon
    assert abs(calculated_delta - expected_delta) < epsilon, f"Calculated Delta: {calculated_delta}\nExpected Delta: {expected_delta}"
    assert abs(calculated_gamma - expected_gamma) < epsilon, f"Calculated Gamma: {calculated_gamma}\nExpected Gamma: {expected_gamma}"
    assert abs(calculated_vega - expected_vega) < epsilon, f"Calculated Vega: {calculated_vega}\nExpected Vega: {expected_vega}"
    assert abs(calculated_theta - expected_theta) < epsilon, f"Calculated Theta: {calculated_theta}\nExpected Theta: {expected_theta}"
    assert abs(calculated_rho - expected_rho) < epsilon, f"Calculated Rho: {calculated_rho}\nExpected Rho: {expected_rho}"