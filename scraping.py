from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

shopee_link = 'https://shopee.co.id/search?keyword=tas%20pria'
driver.set_window_size(1300,800)
driver.get(shopee_link)

# berapa panjang scroll kebawah
rentang = 500
# dibuat sampai 7 agar (1 sampai 6)
for i in range(1,7):
    akhir = rentang * i
# buat perintah menggunakan javascript
    perintah = "window.scrollTo(0,"+str(akhir)+")"
    driver.execute_script(perintah)
    print("loading ke-"+str(i))
    time.sleep(1)

time.sleep(10)

driver.save_screenshot('home.png')
content = driver.page_source
driver.quit()

data = BeautifulSoup(content, 'html.parser')
# print(data.encode('utf-8'))

i = 1
base_url = 'https://shopee.co.id'

list_nama_produk, list_harga_produk, list_lokasi_penjualan, list_produk_terjual, list_link_penjualan=[],[],[],[],[]

for area in data.find_all('div',class_="col-xs-2-4 shopee-search-item-result__item"):
    print('proses data ke-'+str(i))
    nama_produk = area.find('div',class_="ie3A+n bM+7UW Cve6sh").get_text()
    harga_produk = area.find('span',class_='ZEgDH9').get_text()
    lokasi_penjualan = area.find('div',class_='zGGwiV').get_text()
    produk_terjual = area.find('div',class_='r6HknA uEPGHT')
    if produk_terjual != None:
        produk_terjual = produk_terjual.get_text()
    link_penjualan = base_url + area.find('a')['href']

    list_nama_produk.append(nama_produk)
    list_harga_produk.append(harga_produk)
    list_lokasi_penjualan.append(lokasi_penjualan)
    list_produk_terjual.append(produk_terjual)
    list_link_penjualan.append(link_penjualan)
    i+=1
    print("------")

df = pd.DataFrame({"Nama":list_nama_produk,"harga":list_harga_produk,"lokasi":list_lokasi_penjualan,"Produk":list_produk_terjual,"link":list_link_penjualan})
writer = pd.ExcelWriter('TasPria.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()