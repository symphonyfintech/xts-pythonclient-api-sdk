import numpy as np

class MovingAverageCrossoverStrategy:
    def __init__(self, short_ma_period=50, long_ma_period=100):
        self.short_ma_period = short_ma_period
        self.long_ma_period = long_ma_period
        self.position = None
        self.previous_signal = None

    def calculate_moving_averages(self, data):
        short_ma = np.mean(data[-self.short_ma_period:])
        long_ma = np.mean(data[-self.long_ma_period:])
        return short_ma, long_ma

    def generate_signal(self, short_ma, long_ma):
        if short_ma > long_ma and self.previous_signal != 'buy':
            self.position = 'buy ATM Call Option, sell ATM Put Option'
            self.previous_signal = 'buy'
            return 'Buy Signal'
        elif short_ma < long_ma and self.previous_signal != 'sell':
            self.position = 'buy ATM Put Option, sell ATM Call Option'
            self.previous_signal = 'sell'
            return 'Sell Signal'
        else:
            return 'No Signal'

    def execute_trade(self):
        if self.position:
            print(f"Position: {self.position}")
            # Place your trade execution logic here

# Example usage
if __name__ == "__main__":
    # Example historical hourly closing prices for NIFTY MID SELECT index (replace with your own data)
    historical_prices = [...]  # List of historical prices

    strategy = MovingAverageCrossoverStrategy()

    # Assume that we receive hourly closing prices continuously
    for price in historical_prices:
        short_ma, long_ma = strategy.calculate_moving_averages(historical_prices)
        signal = strategy.generate_signal(short_ma, long_ma)
        print(f"Current Price: {price}, Short MA: {short_ma}, Long MA: {long_ma}, Signal: {signal}")
        strategy.execute_trade()
