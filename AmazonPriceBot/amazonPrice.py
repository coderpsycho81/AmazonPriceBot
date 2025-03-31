# CODERPSYCHO #
# https://coderpsycho.psychotr.com/

# INDIRELECEK KÜTÜPHANELER (LIBRARIES TO DOWNLOAD) #
    # pip install requests mysql-connector-python beautifulsoup4 selenium webdriver-manager

# Gerekli Olan Yerleri Doldurunuz. Telegram Chat API ve chat_id (Fill in the required fields. Telegram Chat API and chat_id)
    # Chat API için telegramdan @BotFather kullanın kendinize bir Chat oluşturun ve API bilgilerini doldurunuz. (For the Chat API, use @BotFather from telegram, create a Chat for yourself and fill in the API information.)
    # chat_id içinde oluşturmuş olduğunuz botun chat kısmına /start yazarak komut gönderin ve attığım asd.py dosyasını çalıştırın o sizin chat_id niziverecektir. (Send a command by typing /start in the chat section of the bot you created in chat_id and run the asd.py file I threw and it will give your chat_id.)

# DB_CONFIG MySql ayarları (DB_CONFIG MySql settings)
    # Eğer MySql de veri tabanınız yoksa localhostdan bağlanarak DB_CONFIG i localhost bilgileri ile doldurup çalıştırabilirsiniz. (If you do not have a database in MySql, you can connect from localhost and fill DB_CONFIG with localhost information and run it.)

# Mysql Table Kodları (Mysql Table Codes)
    # CREATE TABLE amazon (
    #   id INT AUTO_INCREMENT PRIMARY KEY,
    #   name VARCHAR(255) NOT NULL,
    #   url VARCHAR(500) NOT NULL
    #   );

    # CREATE TABLE AmazonSettings (
    #   id INT AUTO_INCREMENT PRIMARY KEY,
    #   check_interval INT NOT NULL
    #   );

    # CREATE TABLE price_history (
    #   id INT AUTO_INCREMENT PRIMARY KEY,
    #   name VARCHAR(255) NOT NULL,
    #   price DECIMAL(10,2) NOT NULL,
    #   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #   );

# Program Kullanım (Program Usage)
    # ilk olarak sql den amazon table ınıza amazondaki ürününüzü giriniz. (First, enter your product in amazon from sql to your amazon table.)
    # AmazonSettings table ından da sorgu atacak süreyi giriniz max 60 yeterlidir lakin verileriniz fazlaysa yükseltmekde fayda var (Enter the time to throw a query from the AmazonSettings table, max 60 is enough, but if your data is more, it is useful to increase it.)
    # Ondan sonra kullandığınız editörden projeyi çalıştırın ve bekleyin bu kadar fiyat artınca yada azalınca size bildirim gönderilecektir. (Then run the project from the editor you use and wait, you will be notified when the price increases or decreases.)
    # test etmek içinde price_history table ından verinin fiyatını değiştirmeniz yeterli olucaktır. (Then run the project from the editor you use and wait, you will be notified when the price increases or decreases.)


import requests
import mysql.connector
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

TELEGRAM_TOKEN = ""
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

DB_CONFIG = {
    'host': '',
    'user': '',
    'password': '',
    'database': '',
    'port': 3306
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_amazon_price(url):
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    try:
        price_element = driver.find_element(By.CLASS_NAME, "a-price-whole")
        price = price_element.text.replace(',', '').strip()
    except Exception:
        price = None
    
    driver.quit()
    return price

def get_check_interval():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT check_interval FROM Amazonsettings WHERE id = 1")
        interval = cursor.fetchone()
        if interval:
            return interval[0]  
        else:
            return 60  
    except mysql.connector.Error as e:
        print(f"❌ Veritabanı hatası: {e}")
        return 60 
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def check_prices():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, url FROM amazon")
        products = cursor.fetchall()

        for name, url in products:
            new_price = get_amazon_price(url)  
            if new_price is None:
                continue  

            cursor.execute("SELECT price FROM price_history WHERE name = %s ORDER BY id DESC LIMIT 1", (name,))
            last_price = cursor.fetchone()

            if last_price:
                old_price = int(last_price[0]) 
            else:
                old_price = None  

            if old_price is None: 
                cursor.execute("INSERT INTO price_history (name, price) VALUES (%s, %s)", (name, new_price))
                conn.commit()
                send_telegram_notification(name, url, None, new_price) 
            elif old_price != int(new_price): 
                cursor.execute("UPDATE price_history SET price = %s WHERE name = %s ORDER BY id DESC LIMIT 1", (new_price, name))
                conn.commit()
                send_telegram_notification(name, url, old_price, new_price)  

    except mysql.connector.Error as e:
        print(f"❌ Veritabanı hatası: {e}")
        time.sleep(5)  
        check_prices()  

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def send_telegram_notification(name, url, old_price, new_price):
    if old_price:
        message = f"📢 Ürün: {name}\n🔻 Eski Fiyat: {old_price} TL\n💰 Yeni Fiyat: {new_price} TL\n🔗 {url}"
    else:
        message = f"📢 Ürün: {name}\n💰 Yeni Fiyat: {new_price} TL\n🔗 {url}"

    requests.get(f"{API_URL}sendMessage", params={"chat_id": "chat_id giriniz", "text": message})


if __name__ == "__main__":
    while True:
        check_prices()
        interval = get_check_interval() 
        time.sleep(interval)  
