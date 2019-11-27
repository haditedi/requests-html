import pandas as pd 
from matplotlib import pyplot as plt

df = pd.read_csv('cheval.csv')

plt.plot(df['Date'], df['Chc1bed'], label='Cheval 1 bed')
plt.plot(df['Date'], df['Chc2bed'], label='Cheval 2 bed')
plt.plot(df['Date'], df['Ash1bed'], label='Ashburn 1 bed')

plt.xlabel("Date")
plt.ylabel("Rate")

# plt.style.use("fivethirtyeight")

plt.legend()
plt.show()

