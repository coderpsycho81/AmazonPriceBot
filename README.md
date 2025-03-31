# AmazonPriceBot
This Amazon price tracking bot regularly checks the prices of selected products and sends notifications when changes occur. The bot stores product data in a MySQL database and records price history. Users can view products and get the latest price information via Telegram. 🚀


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
