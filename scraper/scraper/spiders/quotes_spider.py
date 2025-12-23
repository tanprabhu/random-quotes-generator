import scrapy

class QuotesSpider(scrapy.Spider):
  # spider's name - scrapy uses it to identify which spider to run
  name = "quotes"
  # list of urls from which spider will start scraping
  start_urls = ['http://quotes.toscrape.com']

  # extraction logic - how content of page is processed
  def parse(self, response):
    for quote in response.css('div.quote'):
      yield{
        'text': quote.css('span.text::text').get(),
        'author': quote.css('span.small::text').get(),
        'tags': quote.css('div.tags a.tag::text').getall()
      }
      #  pagination
      next_page = response.css('li.next a::attr(href)').get()
      if next_page is not None:
        yield response.follow(next_page, self.parse)






# for handling dynamic content -> Scrapy-splash or Scrapy-selenium
#  scrapy cant execute JSso we need a headless browser for web scraping