from bs4 import BeautifulSoup
import requests
import pandas as pd

# Headers (bazı siteler için bot engelleme sebebiyle headers göndermek gerekebilir)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

# Boş bir liste oluştur ve tüm ürün bilgilerini burada sakla
all_products = []

# 1'den 11'e kadar sayfaları gez
for page_num in range(1, 12):
    # Sayfa URL'si (sayfa numarasını dinamik olarak ekliyoruz)
    url = f"https://www.carrefoursa.com/sarkuteri/c/1070?q=%3AbestSeller&page={page_num}"

    # Web sayfasına istek gönder
    response = requests.get(url, headers=headers)

    # Eğer istek başarılı olduysa (status_code 200), devam et
    if response.status_code == 200:
        # Sayfanın HTML içeriğini al
        soup = BeautifulSoup(response.text, "html.parser")

        # Ürünleri bul
        product_items = soup.find_all("li", class_="product-listing-item")

        # Her bir ürünü döngüye al ve ismi ve fiyatını çek
        for item in product_items:
            # Ürün ismi
            name = item.find("span", class_="item-name").text.strip()

            # Ürün fiyatı (itemprop="price" içeren span'den çekiyoruz)
            price_span = item.find("span", class_="item-price", itemprop="price")
            if price_span:
                price = price_span.get("content")  # Fiyatı content niteliğinden al
            else:
                price = "Fiyat bilgisi yok"

            # Ürün bilgilerini bir listeye ekle
            all_products.append({
                "Ürün İsmi": name,
                "Fiyat": price
            })
        
        print(f"Sayfa {page_num} tamamlandı.")
    else:
        print(f"Web sayfasına erişim başarısız oldu. Status code: {response.status_code}")

# Tüm ürün bilgilerini bir DataFrame'e dönüştür
df = pd.DataFrame(all_products)

# DataFrame'i göster (veya kaydet)
print(df)

df.head()
df.to_csv("carrefoursa_urunler.csv", index=False)

