from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
options = Options()
# options.add_argument("--headless") tanpa membuka browser
options.add_argument('window-size=1200x600') # membuka browser
driver = webdriver.Chrome(options=options)

# driver = webdriver.Chrome()
driver.get("https://www.indopremier.com/ipotstock/marketanalysis.php?page=stockscreener")

# select selectMarketCap
def Menu_Fundamental(jenis,option,tipe,input=2,jenis1="default",option1=2,jenis2="default",option2=2):
    driver.find_element_by_xpath('//*[@id="select%s"]/option[%s]'%(jenis,option)).click()
    if tipe == 1:
        select = driver.find_element_by_xpath('//*[@id="text%s"]'%jenis)
        select.send_keys(Keys.CONTROL, "a")
        select.send_keys(input)
    elif tipe == 2:
        pass
    elif tipe == 3:
        driver.find_element_by_xpath('//*[@id="select%s"]/option[%s]'%(jenis1,option1)).click()
        driver.find_element_by_xpath('//*[@id="select%s"]/option[%s]'%(jenis2,option2)).click()
    else:
        driver.find_element_by_xpath('//*[@id="select%s"]/option[%s]'%(jenis1,option1)).click()
        select = driver.find_element_by_xpath('//*[@id="text%s"]'%jenis2)
        select.send_keys(Keys.CONTROL, "a")
        select.send_keys(input)

# option sampe 3 dimulai 2 (Fundamental)
menu = ["MarketCap","ActPBV","AnlRevenue","AnlPBV","AnlNetProfit","AnlEVEBITDA","DebtEquity","ActPER","AnlROA","AnlPER","AnlROE"]
Menu_Fundamental("MarketCap",2,tipe=1,input=100)

# # option sampe 6 dimulai 2 (DOWN FROM HIGH)
# menu2_kolom1 = ["DownTdy","Down6Mn","Down1WK","Down1Yr","Down1Mn","Down3Mn","DownYTD","DownAllTm"]
# Menu_Fundamental("DownTdy",2,tipe=2)

# # option sampe 6 dimulai 2 (UP FROM LOW)
# menu2_kolom2 = ["UpTdy","Up6Mn","Up1WK","Up1Yr","Up1Mn","Up3Mn","UpYTD","UpAllTm"]
# Menu_Fundamental("UpTdy",2,tipe=2)

# # ########################### (TECHNICAL) #############################
# # option sampe 3 dimulai 2 
# # ComparePrice12 baris 1 kolom 2 
# --------------------- Comparing Price & Overlay ----------------------
menu3_kolom2 = ["ComparePrice12","ComparePrice22","ComparePrice32","ComparePrice42","ComparePrice52"]
menu3_kolom1 = ["ComparePrice11","ComparePrice21","ComparePrice31","ComparePrice41","ComparePrice51"]
menu3_kolom3 = ["ComparePrice13","ComparePrice23","ComparePrice33","ComparePrice43","ComparePrice53"]
Menu_Fundamental("ComparePrice12",2,tipe=3,jenis1="ComparePrice11",option1=8,jenis2="ComparePrice13",option2=6)

# ---------------------- Comparing TA with Value -----------------------
menu4_kolom2 = ["CompareTA12","CompareTA22","CompareTA32","CompareTA42","CompareTA52"]
menu4_kolom1 = ["CompareTA11","CompareTA21","CompareTA31","CompareTA41","CompareTA51"]
menu4_kolom3 = ["CompareTA13","CompareTA23","CompareTA33","CompareTA43","CompareTA53"]
Menu_Fundamental("CompareTA52",2,tipe=4,jenis1="CompareTA51",option1=12,input=20,jenis2="CompareTA53")

# Menu_Fundamental("CompareTA_12",2,tipe=4,jenis1="CompareTA_11",option1=1,input=20,jenis2="CompareTA_13")

# --------------------- Comparing Stochastic & RSI ----------------------
menu3_kolom2 = ["CompareStochastic12","CompareStochastic22"]
menu3_kolom1 = ["CompareStochastic11","CompareStochastic21"]
menu3_kolom3 = ["CompareStochastic13","CompareStochastic23"]
Menu_Fundamental("CompareStochastic12",2,tipe=3,jenis1="CompareStochastic11",option1=3,jenis2="CompareStochastic13",option2=4)

driver.execute_script("submitStockScreen()")
time.sleep(5)
tbl_full = driver.find_element_by_xpath('//*[@id="stockScreenerResult_length"]/label/select/option[5]').click()
time.sleep(5)
tbl = driver.find_element_by_xpath('//*[@id="stockScreenerResult"]').get_attribute('outerHTML')
df = pd.read_html(tbl,header=[0],flavor='bs4')[0]
df.to_csv("trili.csv",)
print(df)
driver.close()

import yfinance as yf
data_saham = pd.read_csv('trili.csv')# df['Stock']
stocks = data_saham['Stock'].tolist()
for i in stocks:
    data_saham['Stock'].replace(to_replace=i, value="%s.JK"%i, inplace=True)
print (data_saham)
for i in data_saham['Stock']:    
    data = yf.download(i, start="2019-01-01", end="2020-04-30")
    data.to_csv("%s.csv"%i)

# kodisi :
# 1. Kondisi uptrend terjadi bila harga telah melewati (menembus) upper band dan harga penutupan berada di luar band.
#    Kondisi downtrend terjadi bila harga melewati lower band dan ditutup di luar band.
# 2. PSAR kondisi mendalam menghitung berapa lama tran berakhir 
# 3. SMA 5 >= SMA 20 
# https://www.indopremier.com/module/newsSmartSearch.php?code=ERAA
# https://www.indopremier.com/module/saham/include/json-charting.php?code=ERAA&start=02/09/2020&end=08/07/2020
# D/F
# https://www.indopremier.com/module/saham/include/data-brokersummary.php?code=ERAA&start=08/07/2020&end=08/07/2020&fd=D&board=all