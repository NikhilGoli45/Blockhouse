import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from backtester import generate_market_data, generate_orders, calculate_metrics

def main():
    runs = 100
    execution_costs = []
    slippages = []

    for run in range(runs):
        time_periods = 100
        market_data = generate_market_data(time_periods=time_periods)
        num_orders = 5
        execution_intervals = 10
        orders = generate_orders(num_orders, execution_intervals, time_periods)
        total_execution_cost, total_slippage = calculate_metrics(market_data, orders, execution_intervals)
        execution_costs.append(total_execution_cost)
        slippages.append(total_slippage)

    average_execution_cost = np.mean(execution_costs)
    average_slippage = np.mean(slippages)

    print(f"Average Total Execution Cost over {runs} runs: {average_execution_cost:.2f}")
    print(f"Average Total Slippage over {runs} runs: {average_slippage:.2f}")

if __name__ == "__main__":
    main()
