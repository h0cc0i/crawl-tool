import scrapy
import pyrebase

menus = []
categories = []
post = []


class bikaeweb(scrapy.Spider):
    name = "hoctiengnhat"

    def __init__(self):

        config = {
            "apiKey": "AIzaSyBaNpQCQK10S2Xm5_0EnheM3-Cm1qH9VkY",
            "authDomain": "crawler-22035.firebaseapp.com",
            "databaseURL": "https://crawler-22035.firebaseio.com",
            "storageBucket": "crawler-22035.appspot.com",
            "serviceAccount": "crawler-firebase-adminsdk.json"
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        token = auth.create_custom_token(config["apiKey"])
        self.db = firebase.database()

    def start_requests(self):
        urls = [
            # 'https://bikae.net/category/doi-song/'
            "https://bikae.net/"
            # "https://bikae.net/category/my-pham-lam-dep/",
            # "https://bikae.net/category/am-thuc-mua-sam/",
            # "https://bikae.net/category/di-lai-du-lich/",
            # "https://bikae.net/category/cham-soc-suc-khoe/",
            # "https://bikae.net/category/me-va-be/",
            # "https://bikae.net/category/doi-song/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_menu)

    def parse_menu(self, response):
        if response.xpath('//li[@class="swipe-menu-item"]/a/@href').extract_first() is not None:
            menus = response.xpath('//li[@class="swipe-menu-item"]/a/@href[contains(.,"category")]').extract()
            for menu in menus:
                yield scrapy.Request(url=menu, callback=self.parse_category)

    def parse_category(self, response):
        # count post
        if response.xpath('//h1[@class="entry-title"]/a/@href').extract_first() is not None:
            categories.append(response.xpath('//h1[@class="entry-title"]/a/@href').extract())

        # check next page use recursion
        next_page = response.xpath('//div[@class="nav-next"]/a/@href').extract_first()
        while next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse_category)

        # call each page
        if next_page is None:
            for cate in categories:
                for post in cate:
                    yield scrapy.Request(url=post, callback=self.parse_article)

    def parse_article(self, response):
        id_post = response.xpath('//article/@id').extract_first().replace("post-", "")
        params = {
            'title': response.xpath('//h1[@class="entry-title"]/text()').extract_first(),
            'author': response.xpath('//a[@class="url fn n"]/text()').extract_first(),
            'entry_content': response.xpath('//div[@class="entry-content"]').extract_first(),
            'image': response.xpath('//meta[@property="og:image"]/@content').extract_first(),
            'publish_date': response.xpath('//time[@class="entry-date published"]/@datetime').extract_first()
        }
        self.db.child("post").child(id_post).set(params)
