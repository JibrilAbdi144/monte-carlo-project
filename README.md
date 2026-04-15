# 📈 Monte-Carlo Option Pricer & Risk Analyser

> ✨ **Live Demo:** [Click here to try the new interactive dashboard!](https://monte-carlo-options-pricing-76douzrylgmmpgxymv4oem.streamlit.app/) \
>   *Price European call & put options, Calculate Greeks & View Price Distributions with user-friendly inputs*


## 🔍 Overview

Monte-carlo simulator using Brownian motion to simulate stochastic asset price behaviour and price European option pay-offs.

## 🗒️ Features
- **:game_die: Monte-Carlo Simulation:** Runs multiple Monte-Carlo simulations of asset prices in parallel to estimate European option pay-off.
- **:microscope: Black-Scholes Validation:** Calculates analytic Black-Scholes solution to compare with Monte-Carlo simulation.
- **:level_slider: Multiple Parameters:** Asset price, strike price, time to maturity, risk-free rate, asset volatility and option type (call or put) can all be changed while subject to robust input validation.
- **:chart_with_downwards_trend: Convergence Analysis:** Plots relative error sizes against number of simulations to study convergence rates.
- **:bar_chart: Interactive Dashboard:** Live web app with dynamic parameter inputs and histogram of asset prices at maturity.
- **:jigsaw: Volatility Calibration:** 

## :books: Mathematical Theory
- **Stochastic Calculus:**  Closed-form solution of Geometric Brownian Motion (GBM) to simulate asset price behaviour.
- **Finite-Difference Numerical Methods:** Central First-Order & Second-Order Approximations with Common Random Numbers (CRMs) to calculate Greeks with reduced noise.
- **Bisection Method:** Stable, robust non-linear equation solver to calculate volatility of an asset using real-world European option parameters.

## :exclamation: Key Results

Monte-Carlo price approaches Black-Scholes price as simulation count increases. At 100,000 simulations, the error is almost guranteed to be less than 1%.

|        Pathway Count         |  Mean of Monte Carlo Prices  |     Black Scholes Price      |        Absolute Error        |       Percentage Error       |
|:----------------------------:|:----------------------------:|:----------------------------:|:----------------------------:|:----------------------------:|
|             1000             |            11.65             |            10.45             |             1.20             |            11.52             |
|             2000             |            10.51             |            10.45             |             0.06             |             0.55             |
|             4000             |            10.29             |            10.45             |             0.16             |             1.51             |
|             8000             |            10.35             |            10.45             |             0.10             |             0.92             |
|            16000             |            10.56             |            10.45             |             0.11             |             1.02             |
|            32000             |            10.39             |            10.45             |             0.06             |             0.62             |
|            64000             |            10.41             |            10.45             |             0.04             |             0.36             |
|            128000            |            10.46             |            10.45             |             0.01             |             0.11             |

*(Asset price = 100, Strike price = 100, Time to Maturity = 1, Risk-free Rate = 0.05, Asset Volatility = 0.2, Option Type = "Call")*

## :chart_with_downwards_trend: Convergence Analysis

Created a log-log plot of pathway counts against relative error

- **Observed Gradient**: -0.85 (Theoretical: -0.5)
- **Correlation Coefficient**: 0.85
- **Note**: Steeper gradient is likely a result of variance reduction from taking median across multiple runs.


## :bulb: Lessons Learned

- First implementation was stuck at 4.8% due to forgetting to include the discount factor (exp(-rT)) at the end.
- Fixed by multiplying by the discount factor when calculating the option price from the simulated stock price.
- Median of three runs reduced the error by ~3.5x compared to a single run at 1 million runs.

## :wrench: Usage

```python
from src.simulator import OptionSimulator
option_price = OptionSimulator(stock=100, strike=100, time=1, rate=0.05, sigma=0.2, option_type='call')
