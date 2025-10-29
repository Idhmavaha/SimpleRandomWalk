import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd

start=dt.datetime.now()-dt.timedelta(days=365)
end=dt.datetime.now()

ticker='RITES.NS'

df=yf.download(ticker,start,end)
#print(df)

logReturn=df['Close'].apply(np.log).diff().dropna()
tradingDays=250

dailyDrift=logReturn.mean()
dailyVolatility=logReturn.std()

muDrift=dailyDrift*tradingDays
sigmaVolatility=dailyVolatility*np.sqrt(tradingDays)

#starting price of simulation
S=df['Close'].iloc[-1]

nextSteps=250
Nsimulations=100

stepPercentage=dailyVolatility

pricePath=np.zeros((nextSteps+1,Nsimulations))
pricePath[0]=S

print(f"Simple random walk for {Nsimulations} paths over {nextSteps} days :\n")
for i in range(Nsimulations):
    currPrice=S

    for t in range(1,nextSteps+1):
        z=np.random.rand()

        if z>=0.5:
            stepFactor=1+stepPercentage
        else:
            stepFactor=1-stepPercentage
        
        currPrice*=stepFactor

        pricePath[t,i]=currPrice

plt.figure(figsize=(12,7))
plt.plot(pricePath)
plt.xlabel("Days into future")
plt.ylabel("Predicted price")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
