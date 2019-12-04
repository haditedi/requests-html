import pandas as pd 
from matplotlib import pyplot as plt

df_ash = pd.read_csv('ashburn.csv')
df_che = pd.read_csv('cheval.csv')

plt.grid(True)

plt.plot(df_ash['Date'], df_ash['Ash1bed'], label='Ashburn 1 bed')
#plt.scatter(df_ash['Date'], df_ash['Ash2bed'], label='Ashburn 2 bed')
#plt.scatter(df_ash['Date'], df_ash['Ash3bed'], label='Ashburn 3 bed')
plt.plot(df_che['Date'], df_che['Chc1bed'], label='Cheval 1 bed')
#plt.scatter(df_che['Date'], df_che['Chc2bed'], label='Cheval 2 bed')

plt.xlabel("Date")
plt.ylabel("Rate")

plt.style.use("fivethirtyeight")
plt.title("Rate Comparison")
plt.legend()
plt.savefig('sample.png')
plt.tight_layout()

plt.show()

#['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']