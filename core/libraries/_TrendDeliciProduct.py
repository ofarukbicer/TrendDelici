import sys
from requests import Session
from parsel import Selector

class TrendDeliciProductException(Exception):
  pass

class TrendDeliciProduct():
  headers = {
    'authority': 'www.trendyol.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'referer': 'https://www.trendyol.com/sr?q=Nk3285507%20Basketbol%20Topu%20280&qt=Nk3285507%20Basketbol%20Topu%20280&st=Nk3285507%20Basketbol%20Topu%20280&os=1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
  }

  req = Session()

  def __init__(self, url):
    self.req.headers.update(self.headers)
    self.url = url
  
  def get_product_info(self):
    try:
      response = self.req.get(self.url)
      if response.status_code == 200:
        html = response.text
        sel = Selector(text=html)

        favPrice = sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[4]/div/div/span/text()').get()
        if favPrice is None:
          favPrice = sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div/div/div[3]/div[2]/span/text()').get()
          if favPrice is None:
            favPrice = sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div/div/div/div[2]/span/text()').get()
            if favPrice is None:
              favPrice = sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[4]/div[2]/div/span[2]/text()').get()
              if favPrice is None:
                favPrice = sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[4]/div/div/div/div[2]/span/text()').get()
                if favPrice is None:
                  favPrice = sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div/div/span/text()').get()
        if "," in favPrice:
          favPrice = float(str(favPrice).replace(",", ".").replace("TL", "").strip())
        else:
          favPrice = int(str(favPrice).replace("TL", "").strip())
        product_info = {
          'brandName': str(sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/h1/a/text()').get()).strip(),
          'contentId': int(self.url.split('?')[0].split('-p-')[-1]),
          'contentName': str(sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/h1/span/text()').get()).strip(),
          'favoritedPrice': favPrice,
          'categoryId': int(str(sel.xpath('//*[@id="dsa-category-id"]/div/text()').get()).strip().rstrip("/").split("/")[-1]),
          'categoryName': str(sel.xpath('//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/text()').get()).strip().replace(" kategorisinde", ""),
        }
        return product_info
      return None
    except Exception as e:
      tb = sys.exc_info()[2]
      raise TrendDeliciProductException(f'TrendDeliciProductException: get_product_info() -> {e}').with_traceback(tb)