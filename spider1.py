import scrapy
valid = True


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        global valid
        urls = [
            'https://usawatchdog.com/'
        ]

        for url in urls:
            valid = True
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        allLinks = response.css('.title a::attr(href)').getall()

        for each_link in allLinks:
            yield scrapy.Request(each_link, callback=self.parse_href)

        if valid:
            next_page = response.css('.pagination a::attr(href)')[-2].get()
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_href(self, response):
        global valid
        yearsList = ['2021', '2020', '2019', '2018']
        available = False
        date = response.css('.thetime::text').get()
        if date is not None:
            date = date.replace('On ', '')
            for year in yearsList:
                if year in date:
                    available = True
                    break
        if available:
            title = response.css('.title::text').get()
            paragraph = response.css('.post-single-content p::text').getall()
            text = ''
            count = 0
            for sentence in paragraph:
                if count == 3:
                    break
                sentence = sentence.replace('\xa0', '')
                sentence = sentence.replace('\n', '')
                sentence = sentence.replace('\r', '')
                sentence = sentence.replace('\t', '')
                if sentence != "":
                    text = text + sentence
                    count += 1
            yield {
                'date': date,
                'title': title,
                'text': text,
                'is_fake': 1
            }
        elif date is not None:
            valid = False
