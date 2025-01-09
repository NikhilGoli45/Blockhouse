import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_market_data(time_periods=100, start_price=100, volatility=1, num_venues=3):
    #np.random.seed(24) #uncomment this line to fix market movements
    baseline_changes = np.random.normal(0, volatility, time_periods)
    baseline_prices = np.cumsum(baseline_changes) + start_price

    data = []
    for venue_id in range(1, num_venues + 1):
        venue_noise = np.random.normal(0, volatility * 0.2, time_periods)
        prices = baseline_prices + venue_noise
        volumes = np.random.randint(0, 1000, time_periods)

        venue_data = pd.DataFrame({
            "Timestamp": range(time_periods),
            "Price": prices,
            "Volume": volumes,
            "Venue": f"Venue_{venue_id}"
        })
        data.append(venue_data)
    return pd.concat(data, ignore_index=True)

def generate_orders(num_orders, execution_intervals, time_periods):
    order_size = np.random.randint(500, 2000, size=num_orders)
    max_start_time = time_periods - execution_intervals
    time_of_placement = np.random.choice(range(max_start_time), size=num_orders, replace=False)
    return pd.DataFrame({"Order_ID": [f"Order_{i+1}" for i in range(num_orders)], "Order_Size": order_size, "Time_of_Placement": time_of_placement})

def calculate_metrics(market_data, orders, execution_intervals):
    market_data["VWAP"] = np.nan

    for timestamp in market_data["Timestamp"].unique():
        vwap_data = market_data[(market_data["Timestamp"] >= timestamp - 5) & (market_data["Timestamp"] <= timestamp)]
        total_volume = vwap_data["Volume"].sum()
        if total_volume > 0:
            vwap = (vwap_data["Price"] * vwap_data["Volume"]).sum() / total_volume
            market_data.loc[market_data["Timestamp"] == timestamp, "VWAP"] = vwap

    execution_results = []
    for _, order in orders.iterrows():
        start_time = order["Time_of_Placement"]
        end_time = start_time + execution_intervals
        time_range_data = market_data[(market_data["Timestamp"] >= start_time) & (market_data["Timestamp"] < end_time)]
        best_venue_data = time_range_data.groupby("Timestamp").apply(lambda x: x.loc[x["Price"].idxmin()])
        next_time_data = market_data[market_data["Timestamp"] == end_time]

        if not next_time_data.empty:
            actual_execution_price = (best_venue_data["Price"].min() + next_time_data["Price"].min()) / 2
        else:
            actual_execution_price = best_venue_data["Price"].min()

        expected_execution_price = best_venue_data["Price"].min()
        vwap = time_range_data["VWAP"].mean()
        execution_cost = actual_execution_price - vwap
        slippage_amount = expected_execution_price - actual_execution_price

        execution_results.append({
            "Order_ID": order["Order_ID"],
            "Order_Size": order["Order_Size"],
            "Time_of_Placement": order["Time_of_Placement"],
            "Execution_Cost": execution_cost,
            "Slippage": slippage_amount
        })

    total_execution_cost = sum([result["Execution_Cost"] for result in execution_results])
    total_slippage = sum([result["Slippage"] for result in execution_results])

    for result in execution_results:
        print(f"{result['Order_ID']} - Size: {result['Order_Size']} placed at {result['Time_of_Placement']}:")
        print(f"  Execution Cost: {result['Execution_Cost']:.2f}")
        print(f"  Slippage: {result['Slippage']:.2f}")

    print("\nCumulative Metrics:")
    print(f"  Total Execution Cost: {total_execution_cost:.2f}")
    print(f"  Total Slippage: {total_slippage:.2f}")

def main():
    time_periods = 100
    market_data = generate_market_data(time_periods=time_periods)
    num_orders = 5
    execution_intervals = 10
    orders = generate_orders(num_orders, execution_intervals, time_periods)
    calculate_metrics(market_data, orders, execution_intervals)

    plt.figure(figsize=(10, 6))
    venues = market_data["Venue"].unique()
    for venue in venues:
        venue_data = market_data[market_data["Venue"] == venue]
        plt.plot(venue_data["Timestamp"], venue_data["Price"], label=f"{venue} Price")

    plt.plot(market_data["Timestamp"].unique(), market_data.drop_duplicates("Timestamp")["VWAP"], color="orange", label="Dynamic VWAP (All Venues)")

    for _, order in orders.iterrows():
        x = order["Time_of_Placement"]
        y = market_data[(market_data["Timestamp"] == x)]["Price"].min()
        plt.scatter(x, y, color="red")
        plt.text(x, y, f"{order['Order_ID']}", fontsize=8, ha="right", va="bottom", color="blue")

    plt.title("Market Prices vs Dynamic VWAP with Order Placements")
    plt.xlabel("Minutes")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
