import scrapy

class MidsouthShootersSpider(scrapy.Spider):
    name = 'MidsouthShooters'
    page_number = 2
    start_urls = ['https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1']

    def parse(self, response):
        for products in response.css('div.product'):
            yield {
                'price' : float(products.css('span.price').css('span::text').get().replace('$', '')),
                'title' : products.css('a.catalog-item-name::text').get(),
                'stock' : False if products.css('span.status').css('span::text').get() == 'Out of Stock' else True, 
                'maftr' : products.css('a.catalog-item-brand::text').get()                
            }
        next_page = 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=' + str(MidsouthShootersSpider.page_number)
        if MidsouthShootersSpider.page_number < 3:
            yield response.follow(next_page, callback = self.parse)