# Importing basic python modules
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Importing from modules in this project
# to perform the calculations
from src.black_scholes import calculateBlackScholesPrice
from src.monte_carlo import calculateMonteCarloPrice
from src.greeks import calculateDerivative
from src.data_models import validateParameters

if "results" not in st.session_state:
    st.session_state["results"] = None

if st.session_state["results"]:
    result = st.session_state["results"]


# Title of the Streamlit dashboard
st.title("Monte-Carlo European Option Pricer")

with st.form("my_form"):

    # Sidebar that allows the user to input
    # their own custom parameters
    st.sidebar.header("Option Parameters")
    stock = st.sidebar.number_input(label="Stock Price (S)", min_value=0., value=100.)
    strike = st.sidebar.number_input(label="Strike Price (K)", min_value=0., value=100.)
    time = st.sidebar.number_input(label="Time to Maturity (T)", min_value=0., value=1.)
    rate = st.sidebar.number_input(label="Risk-free Rate (r)", value=0.05)
    sigma = st.sidebar.number_input(label="Volatility (sigma)", min_value=0., value=0.2)
    option_type = st.sidebar.radio(label="Option Type", options=["call", "put"])
    simulation_count = st.sidebar.number_input(label="Number of Simulations", min_value=1, value=100000)

    option_parameters = {
        "stock": stock,
        "strike": strike,
        "time": time,
        "rate": rate,
        "sigma": sigma,
        "option_type": option_type.lower()
    }

    calculate_button = st.form_submit_button(label="Calculate", type="primary", use_container_width=True)

    if calculate_button:
        with st.spinner("Running Monte-Carlo Simulation: "):

            try:
                validateParameters(option_parameters=option_parameters)


                random_seed = np.random.normal(size=simulation_count)
                final_stock_prices = calculateMonteCarloPrice(random_seed=random_seed, option_parameters=option_parameters, return_stock=True)
                mean_monte_carlo_price = np.mean(calculateMonteCarloPrice(random_seed=random_seed, option_parameters=option_parameters))
                black_scholes_price = calculateBlackScholesPrice(option_parameters=option_parameters)
                absolute_error = np.abs(mean_monte_carlo_price - black_scholes_price)
                percentage_error = 100 * absolute_error / black_scholes_price

                greeks = {}
                greeks["delta"] = calculateDerivative(random_seed=random_seed, option_parameters=option_parameters, parameter_type="stock")
                greeks["gamma"] = calculateDerivative(random_seed=random_seed, option_parameters=option_parameters, parameter_type="stock", derivative_type=2)
                greeks["vega"] = calculateDerivative(random_seed=random_seed, option_parameters=option_parameters, parameter_type="sigma", step_size=0.02)
                greeks["theta"] = calculateDerivative(random_seed=random_seed, option_parameters=option_parameters, parameter_type="time", step_size=0.01)
                greeks["rho"] = calculateDerivative(random_seed=random_seed, option_parameters=option_parameters, parameter_type="rate", step_size=0.0001)


                st.session_state["results"] = {
                    "final_stock_prices": final_stock_prices,
                    "mean_monte_carlo_price": mean_monte_carlo_price,
                    "black_scholes_price": black_scholes_price,
                    "absolute_error": absolute_error,
                    "percentage_error": percentage_error,
                    "option_parameters": option_parameters,
                    "greeks": greeks
                }

            except Exception as error:
                st.error(f"Error: {error}")  

            st.rerun()

if st.session_state.get("results"):

    results = st.session_state["results"]

    st.subheader("Main results")

    precision_level = 3
    rows = [st.columns(spec=2)] * 2
    rows[0][0].metric(value=f"{results["mean_monte_carlo_price"]:.{precision_level}f}", label=f"Monte-Carlo Option Price:")
    rows[0][1].metric(value=f"{results["black_scholes_price"]:.{precision_level}f}", label=f"Black-scholes Option Price:")
    rows[1][0].metric(value=f"{results["absolute_error"]:.{precision_level}f}", label="Absolute Error:")
    rows[1][1].metric(value=f"{results["percentage_error"]:.{precision_level}f}", label="Percentage Error:")

    st.divider()

    st.subheader("Greeks")

    greeks_metrics = st.columns(spec=5)

    for index, greek in enumerate(results["greeks"]):
        greeks_metrics[index].metric(label=greek.capitalize(), value=f"{results["greeks"][greek]:.{precision_level}f}")

    # st.metric("Delta", f"{results["delta"]:.{precision_level}f}")
    # st.metric("Gamma", f"{results["gamma"]:.{precision_level}f}")
    # st.metric("Vega", f"{results["vega"]:.{precision_level}f}")
    # st.metric("Theta", f"{results["theta"]:.{precision_level}f}")
    # st.metric("Rho", f"{results["rho"]:.{precision_level}f}")

    with st.expander("View Stock Price Distribution"):

        figure, axes = plt.subplots()
        axes.hist(results["final_stock_prices"], bins=50, alpha=0.75)
        axes.axvline(results["option_parameters"]["strike"], color="red", label=f"Strike Price: K={results["option_parameters"]["strike"]}")

        axes.set_title("Terminal Stock Price Distribution")
        axes.set_xlabel("Stock Price at Maturity")
        axes.set_ylabel("Frequency")

        plt.legend()
        st.pyplot(figure)

    st.success("Calculation successful!")



# if st.session_state["results"] is None:


#     if st.button("Calculate Option Price", type="primary", use_container_width=True):
#         print()

#     else:

#         st.info("Adjust parameters and then press 'Calculate' to see results.")

# else:

#     results = st.session_state["results"]

#     if st.button(label="Recalculate", type="primary", use_container_width=True):
#         st.session_state["results"] = None
#         st.rerun()

    





if st.session_state["results"]:
    monte_carlo_prices = st.session_state["results"]["final_stock_prices"]
    strike_price = st.session_state["results"]["option_parameters"]["strike"]

    

