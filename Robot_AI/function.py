from numpy import r_
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

today = date.today()
d1 = today.strftime("%Y%m%d")
print(d1)

df = pd.read_csv('CafeF.HSX.Upto04.06.2021.csv')

Bank_Hose = ['ACB', 'BID', 'CTG', 'EIB', 'HDB', 'LPB', 'MBB', 'MSB', 'OCB', 'SSB', 'STB', 'TCB', 'TPB', 'VCB', 'VIB', 'VPB']

print(Bank_Hose)

data = df[
            (df['<DTYYYYMMDD>'] >= 20210101) & (df['<Ticker>'].str.contains('|'.join(Bank_Hose)))
          ]

mid = data['<Ticker>'].str[0:3]

print(mid)


data.to_csv('analyze.csv', encoding='utf-8', index=False)

print(data)
#print(data5)

#plt.figure(figsize=(12.5, 4.5))
#plt.plot(data5, label = 'VCB')
#plt.title('Vietcombank. Close History')
#plt.xlabel('2021-01-04, 2021-06-04')
#plt.ylabel('Close price')
#plt.legend(loc='upper left')
#plt.show()


