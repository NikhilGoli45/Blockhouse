This is a simple backtester designed to test a Smart Order Router that uses a TWAP execution strategy.

In order to run this backtester, first ensure you have set up your python virtual environment. This can be done by running `python3 -m venv venv` in your terminal, then restarting your terminal. After you have set up your environment, you will need to install the necessary packages numpy, pandas, and matplotlib. This can be done by running the following commands in your virtual environment: `pip install numpy`, `pip install pandas`, and `pip install matplotlib`. 

Once you have completed this set up, you are now ready to run the backtester. Simply run the command `python3 backtester.py` in your terminal and watch the results display on your screen!

There are some configuration changes that you can make to the backtester in order to change the market simulation behavior. If you want a new random market each time you run the backtester, leave the code on line 6 commented out. However, if you want to view the same market in across multiple runs, uncomment line 6, and choose a seed which can be any random integer. Choosing a seed will not let you control how the market moves since this is a truly random process, however it will maintain this market for as long as the seed is specified.
