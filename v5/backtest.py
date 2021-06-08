import requests as rq
import pandas as pd
from datetime import date, timedelta
import time
import zipfile as zf
import os
from os import path
import shutil
from progress.bar import Bar
from time import process_time
import statistics

ticker_file = 'ticker_hose'
ticker_bad = 'ticker_bad'
ticker_worst = 'ticker_worst'
ticker_moved = 'ticker_moved'
smaHigh = 1.2
smaMed = 0.95
smaLow = 0.8
hadxlv = 25
ladxlv = 15
stoRSIlv = 20
SmoothK = 5

# Doc ngay gio hien tai va dinh dang thanh kieu thich hop
t = time.localtime()
today = date.today()
date = int(today.strftime('%d'))
month = int(today.strftime('%m'))
year = int(today.strftime('%Y'))
today1 = today.strftime('%Y%m') + str(date)
today2 = str(date) + today.strftime('%m%Y')
today3 = str(date) + today.strftime('.%m.%Y')
print('...')
print('Today is {x}/{y}/{z}'.format(x = date, y = month, z = year))
print('...')

# Download du lieu tu CafeF
print('Data downloading...')
url = 'http://images1.cafef.vn/data/{x}/CafeF.SolieuGD.Upto{y}.zip'.format(x = today1, y = today2)
r = rq.get(url)

while r.status_code == 404:
		today -= timedelta(days = 1)
		date = int(today.strftime('%d'))
		month = int(today.strftime('%m'))
		year = int(today.strftime('%Y'))
		today1 = today.strftime('%Y%m') + str(date)
		today2 = str(date) + today.strftime('%m%Y')
		today3 = str(date) + today.strftime('.%m.%Y')
		url = 'http://images1.cafef.vn/data/{x}/CafeF.SolieuGD.Upto{y}.zip'.format(x = today1, y = today2)
		r = rq.get(url)

if r.status_code == 200:
	print('Data date: {x}/{y}/{z}'.format(x = date, y = month, z = year))
	open('raw_data.zip', 'wb').write(r.content)
	print('Data downloaded!')
	print('...')
else:
	print('Data downloading failed. Code: ', r.status_code)
	exit()

# Giai nen, xoa cac file khong can thiet va doi ten file data tho
print('Editing data file...')
with zf.ZipFile('raw_data.zip', 'r') as zip_ref:
	zip_ref.extractall()

os.remove('CafeF.HNX.Upto{}.csv'.format(today3))
os.remove('CafeF.UPCOM.Upto{}.csv'.format(today3))
os.remove('raw_data.zip')
if path.exists('raw_data.csv') == True:
	os.remove('raw_data.csv')
os.rename('CafeF.HSX.Upto{}.csv'.format(today3), 'raw_data.csv')

# Chinh sua ten cot trong data frame
raw_df = pd.read_csv('raw_data.csv')
raw_df.columns = [['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
raw_df.to_csv('raw_data.csv')
print('...')

# Lay danh sach cac ma chung khoan
print('Getting ticker list...')
df = pd.read_csv('raw_data.csv')
ticker_list = list(df['Ticker'])
ticker_list = list(set(ticker_list))

# Loai bo cac cac ma chung khoan khong hop le
remove = list()
for i in ticker_list:
	if len(i) > 3:
		remove.append(i)
for i in remove:
	ticker_list.remove(i)

df = pd.read_csv('{}.txt'.format(ticker_moved), header = None)
df.columns = ['Ticker']
remove = list(df['Ticker'])
for i in remove:
	ticker_list.remove(i)

# Kiem tra ma chung khoan moi
df = pd.read_csv('{}.txt'.format(ticker_file), header = None)
df.columns = ['Ticker']
ticker1 = list(df['Ticker'])
ticker1.sort()
ticker2 = list.copy(ticker_list)

for i in ticker1:
	ticker2.remove(i)

if len(ticker2) != 0:
	print('New ticker: ', ticker2)
	exit()

# Loai bo cac ma chung khoan xau
df = pd.read_csv('{}.txt'.format(ticker_bad), header = None)
df.columns = ['Ticker']
remove = list(df['Ticker'])
for i in remove:
	ticker_list.remove(i)

df = pd.read_csv('{}.txt'.format(ticker_worst), header = None)
df.columns = ['Ticker']
remove = list(df['Ticker'])
for i in remove:
	ticker_list.remove(i)

print('Done! No new ticker')
print('...')

# Phan chia cac ma chung khoan
t0 = process_time()
raw_df = pd.read_csv('raw_data.csv')
if path.exists('Tickers') == True:
	shutil.rmtree('Tickers')
os.mkdir('Tickers')
bar = Bar('Splitting data...', max = len(ticker_list))
for i in range(0, len(ticker_list)):
	ticker = ticker_list[i]
	ticker_df = raw_df[raw_df.Ticker == ticker]
	ticker_df = ticker_df[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
	ticker_df = ticker_df.iloc[::-1]
	ticker_df.to_csv('./Tickers/{}.csv'.format(ticker))
	bar.next()
bar.finish()
t1 = process_time()
print('Data splitted in: ', round(t1 - t0, 2), 'seconds')
print('...')

# Lay thong tin so phien da giao dich cua cac ma chung khoan va xoa cac ma khong du thong tin tinh toan
print('Remove new ticker...')
remove = list()
for i in range(0, len(ticker_list)):
	ticker = ticker_list[i]
	df = pd.read_csv('./Tickers/{}.csv'.format(ticker))
	if len(df) < 1250:
		remove.append(ticker_list[i])
for i in remove:
	ticker_list.remove(i)
	os.remove('./Tickers/{}.csv'.format(i))
print('...')

# Tinh toan cac chi bao ky thuat
t0 = process_time()

# Ticker = list()
# Close = list()
# Action = list()
# Reason = list()

if path.exists('Results') == True:
	shutil.rmtree('Results')
os.mkdir('Results')

bar = Bar('Calculating data...', max = len(ticker_list))
for i in range(0, len(ticker_list)):
	ticker = ticker_list[i]
	# Ticker.append(ticker)
	df = pd.read_csv('./Tickers/{}.csv'.format(ticker))

	d = list(df['Date'])
	o = list(round(df['Open'], 4))
	h = list(round(df['High'], 4))
	l = list(round(df['Low'], 4))
	c = list(round(df['Close'], 4))
	v = list(df['Volume'])
	# Close.append(c[len(c)-1])

	SMA100 = list()
	RSI = list()
	StoRSI = list()
	ADX = list()
	
	for i in range(0, len(c)):
		#SMA100
		if i < 99:
			SMA100.append('x')
		else:
			sma100 = round(c[i]/statistics.mean(c[(i-99):(i+1)]), 4)
			SMA100.append(sma100)	
		
		#RSI
		if i < 14:
			RSI.append('x')
		if i == 14:
			gain = 0
			loss = 0
			for x in range(1, 15):
				if (c[x] - c[x-1]) > 0:
					gain += c[x] - c[x-1]
				elif (c[x] - c[x-1]) < 0:
					loss += c[x-1] - c[x]
			gain /= 14
			loss /= 14
			if loss == 0:
				RSI.append(100)
			else:
				RSI.append(100 - 100/(1 + gain/loss))
		elif i > 14:
			if (c[i] - c[i-1]) > 0:
				gain = (gain*13 + c[i] - c[i-1])/14
				loss = loss*13/14
			elif (c[i] - c[i-1]) < 0:
				gain = gain*13/14
				loss = (loss*13 + c[i-1] - c[i])/14			
			else:
				gain = gain*13/14
				loss = loss*13/14
			if loss == 0:
				RSI.append(100)
			else:
				RSI.append(100 - 100/(1 + gain/loss))

		#ADX
		if i < 14:
			ADX.append('x')
		if i == 14:
			tr = h[0] - l[0]
			for x in range(1, 14):
				tr += max(h[x]-l[x], abs(h[x]-c[x-1]), abs(l[x]-c[x-1]))
			tr /= 14
			tr = (tr*13 + max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1])))/14
			DMu = 0
			DMd = 0
			for x in range(1, 14):
				UM = h[x] - h[x-1]
				DM = l[x-1] - l[x]
				if (UM > DM) and (UM > 0):
					DMu += UM
				elif (UM < DM) and (DM > 0):
					DMd += DM
			DMu /= 14
			DMd /= 14
			DIu = 100*DMu/tr
			DId = 100*DMd/tr
			adx = round(100*abs(DIu - DId)/abs(DIu + DId), 4)
			ADX.append(adx)
		elif i > 14:
			tr = (tr*13 + max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1])))/14
			
			UM = h[i] - h[i-1]
			DM = l[i-1] - l[i]
			if (UM > DM) and (UM > 0):
				DMu = (DMu*13 + UM)/14
				DMd = DMd*13/14
			elif (UM < DM) and (DM > 0):
				DMd = (DMd*13 + DM)/14
				DMu = DMu*13/14
			else:
				DMd = DMd*13/14
				DMu = DMu*13/14

			DIu = 100*DMu/tr
			DId = 100*DMd/tr
			padx = adx
			adx = round((adx*13 + 100*abs(DIu - DId)/abs(DIu + DId))/14, 4)
			ADX.append(adx)

	#StochRSI
	# pstoRSI = 0	
	# for i in range(len(RSI)-SmoothK-1, len(RSI)-1):
	# 	pstoRSI += 100*(RSI[i] - min(RSI[(i-13):(i+1)]))/(max(RSI[(i-13):(i+1)]) - min(RSI[(i-13):(i+1)]))
	# pstoRSI = round(pstoRSI/SmoothK, 4)

	
	for i in range(0, len(RSI)):
		if i < (27 + SmoothK - 1):
			StoRSI.append('x')
		else:
			stoRSI = 0
			for x in range(i - SmoothK + 1, i + 1):
				if (max(RSI[(x-13):(x+1)]) - min(RSI[(x-13):(x+1)])) == 0:
					stoRSI += 100
				else:
					stoRSI += 100*(RSI[x] - min(RSI[(x-13):(x+1)]))/(max(RSI[(x-13):(x+1)]) - min(RSI[(x-13):(x+1)]))
			stoRSI = round(stoRSI/SmoothK, 4)
			StoRSI.append(stoRSI)

	df = pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'SMA100', 'Stoch RSI', 'ADX'])
	df['Date'] = d
	df['Open'] = o
	df['High'] = h
	df['Low'] = l
	df['Close'] = c
	df['Volume'] = v
	df['SMA100'] = SMA100
	df['Stoch RSI'] = StoRSI
	df['ADX'] = ADX
	df = df[-700:-180]

	df.to_csv('./Results/{}.csv'.format(ticker))

	# StoRSI.append(stoRSI)
	# ADX.append(adx)

	# if 	sma100 < smaLow:
	# 	Action.append('Follow')
	# 	Reason.append('Price lower than {}% SMA100'.format(smaLow*100))
	# elif (sma100 > smaMed) and (sma100 < smaHigh):
	# 	if adx >= hadxlv:
	# 		if (pstoRSI < stoRSIlv) or (stoRSI < stoRSIlv):
	# 			if stoRSI >= pstoRSI:
	# 				Action.append('Buy')
	# 				Reason.append('Meet all requirement for buying')
	# 			else:
	# 				Action.append('Follow')
	# 				Reason.append('Stochastic RSI is falling down')
	# 		else:
	# 			Action.append('x')
	# 			Reason.append('x')
	# 	elif (adx >= ladxlv) and (adx < hadxlv):
	# 		if adx >= padx:
	# 			if (pstoRSI < stoRSIlv) or (stoRSI < stoRSIlv):
	# 				Action.append('Follow')
	# 				Reason.append('ADX between {x}-{y}'.format(x = ladxlv, y = hadxlv))
	# 			else:
	# 				Action.append('x')
	# 				Reason.append('x')
	# 		else:
	# 			Action.append('x')
	# 			Reason.append('x')
	# 	else:
	# 		Action.append('x')
	# 		Reason.append('x')
	# else:
	# 	Action.append('x')
	# 	Reason.append('x')

	bar.next()
bar.finish()

# result_df = result_df[result_df['Action'] != 'x']

t1 = process_time()
print('Data calculated in: ', round(t1 - t0, 2), 'seconds')
print('...')

# if path.exists('result-{}.csv'.format(today2)) == True:
# 	os.remove('result-{}.csv'.format(today2))
# result_df.to_csv('result-{}.csv'.format(today2))

# if path.exists('C:/Users/phamt/Desktop/result-{}.csv'.format(today2)) == True:
# 	os.remove('C:/Users/phamt/Desktop/result-{}.csv'.format(today2))
# shutil.copy('result-{}.csv'.format(today2), 'C:/Users/phamt/Desktop')

# if path.exists('E:/Job/Prj/StockRobot/Result/result-{}.csv'.format(today2)) == True:
# 	os.remove('E:/Job/Prj/StockRobot/Result/result-{}.csv'.format(today2))
# shutil.move('result-{}.csv'.format(today2), 'E:/Job/Prj/StockRobot/Result')

if path.exists('Tickers') == True:
	shutil.rmtree('Tickers')
