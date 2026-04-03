# Monte Carlo Option Pricer

## Overview
Monte-carlo simulator using Brownian motion in order to price European option. It validates them against the Black-Scholes analytic solution.


## Key Results

Follwowing table compares the mean price of the Monte-Carlo simulation repeated n times and calculates the percentage error from the Black-Scholes price.

        Pathway Count         |  Mean of Monte Carlo Prices  |     Black Scholes Price      |        Absolute Error        |       Percentage Error       
------------------------------|------------------------------|------------------------------|------------------------------|------------------------------
            10000             |            10.43             |            10.45             |             0.02             |             0.22
            19306             |            10.47             |            10.45             |             0.02             |             0.22
            37275             |            10.50             |            10.45             |             0.04             |             0.43
            71968             |            10.48             |            10.45             |             0.03             |             0.29
            138949            |            10.42             |            10.45             |             0.03             |             0.27
            268269            |            10.45             |            10.45             |             0.00             |             0.00
            517947            |            10.45             |            10.45             |             0.00             |             0.05
           1000000            |            10.47             |            10.45             |             0.02             |             0.15

## Convergence Analysis

Created a log-log plot of pathway counts against relative error

- **Observed Gradient**: -0.85 (Theoretical: -0.5)
- **Correlation Coefficient**: 0.85
- **Note**: Steeper gradient is likely a result of variance reduction from taking median across multiple runs.


## Lessons Learned

- First implementation was stuck at 4.8% due to forgetting to include the discount factor (exp(-rT)) at the end.
- Fixed by multiplying by the discount factor when calculating the option price from the simulated stock price.
- Median of three runs reduced the error by ~3.5x compared to a single run at 1 million runs.


## Usage

```python
from src.simulator import OptionSimulator
option_price = OptionSimulator(stock=100, strike=100, time=1, rate=0.05, sigma=0.2, option_type='call')


