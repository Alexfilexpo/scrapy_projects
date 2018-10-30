import scrapy

class google_spider(scrapy.Spider):
    name = "google_play_apps_info"

    host = "https://play.google.com"

    start_urls = [
        "https://play.google.com/store/apps?hl=en",
    ]

    def parse(self, response):
        categories = response.xpath('//div[contains(@jsinstance, "1")]/div[contains(@jsl, "$x 5;$t t-QH4hoG9vrLo;$x 0;")]//ul/li')
        for category in categories:
            category_href = category.xpath('./div/a/@href').extract_first()
            category_url = "{}{}".format(self.host, category_href)
            yield response.follow(category_url, self.parse_games)

    def parse_games(self, response):
        category = response.xpath('//span[contains(@jsan, "7.title")]/text()').extract_first()
        games_list = response.xpath(
            '//div[contains(@class, "id-cluster-container")]/div/div[contains(@class, "id-card-list")]/div')
        for game in games_list:
            game_name = game.xpath(
                './div/div[contains(@class, "details")]/a[contains(@class, "title")]/@title').extract_first()
            game_link = game.xpath(
                './div/div[contains(@class, "details")]/a[contains(@class, "card-click-target")]/@href').extract_first()
            valid_game_link = '{}{}'.format(self.host, game_link)
            game_developer = game.xpath('./div/div[contains(@class, "details")]/div/a/@title').extract_first()
            yield {
                'Category': category,
                'Name': game_name,
                'Developer': game_developer,
                'Link': valid_game_link,
            }
