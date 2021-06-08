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

today = date.today()
d1 = today.strftime("%Y%m%d")
print(d1)

t = time.localtime()
today = date.today()
date = str(today.strftime('%d'))
month = str(today.strftime('%m'))
year = str(today.strftime('%Y'))
today1 = today.strftime('%Y%m') + date
today2 = date + today.strftime('%m%Y')
today3 = date + today.strftime('.%m.%Y')
print('...')
print('Today is {x}/{y}/{z}'.format(x = date, y = month, z = year))
print('...')

#download du lieu trong ngay 
print('Data downloading...')
url = 'http://images1.cafef.vn/data/{x}/CafeF.SolieuGD.Upto{y}.zip'.format(x = today1, y = today2)
r = rq.get(url)
print(url)

#404 loi ko xac dinh ngay vi du lieu muon down qua moi. Set lai ngay truoc do
while r.status_code == 404:
		today -= timedelta(days = 1)
		date = str(today.strftime('%d'))
		month = str(today.strftime('%m'))
		year = str(today.strftime('%Y'))
		today1 = today.strftime('%Y%m') + date
		today2 = date + today.strftime('%m%Y')
		today3 = date + today.strftime('.%m.%Y')
		url = 'http://images1.cafef.vn/data/{x}/CafeF.SolieuGD.Upto{y}.zip'.format(x = today1, y = today2)
		r = rq.get(url)
    
print(url)

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

os.remove('CafeF.HNX.Upto{}.csv'.format(today3)) #remove san HNX
os.remove('CafeF.UPCOM.Upto{}.csv'.format(today3)) #remove san UPCOM
os.remove('raw_data.zip')
if path.exists('raw_data.csv') == True:
	 os.remove('raw_data.csv')
os.rename('CafeF.HSX.Upto{}.csv'.format(today3), 'raw_data.csv')