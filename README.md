# Monte Carlo Option Pricer

## Overview
Monte-carlo simulator using Brownian motion in order to price European option. It validates them against the Black-Scholes analytic solution.


## Key Results

Follwowing table compares the mean price of the Monte-Carlo simulation repeated n times and calculates the percentage error from the Black-Scholes price.

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


