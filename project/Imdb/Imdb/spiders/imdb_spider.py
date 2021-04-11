import json
import scrapy
from bs4 import BeautifulSoup


class ImdbSpider(scrapy.Spider):
    name = 'imdb'

    start_urls = ['https://m.imdb.com/title/tt8421350/reviews']

    def start_request(self):

        for url in urls:
            yield scrapy.request(url)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'imdb_reviews_{0:s}.json'.format(page)

        bs = BeautifulSoup(response.body)

        div1 = bs.find('div', {'id': 'pagecontent'})
        div2 = div1.find('div', {'class': 'container'})
        div3 = div2.find('div', {'class': 'row'})
        section = div3.find('section', {'class': 'col-xs-12 lister'})
        ul = section.find('ul', {'class': 'ipl-content-list row'})
        div4 = ul.find('div', {'id': 'reviews-container'})
        li = div4.find_all('li', {'class': 'ipl-content-list__item'})

        self.log('----------------------------------------')
        data = {}
        it_review = 1
        for i, l in enumerate(li):
            div5 = l.find('div', {'class': 'imdb-user-review'})
            div6 = div5.find('div')
            div7 = div6.find('div', {'class': 'content'})
            date1 = div6.find('div', {'class': 'review-header'})
            date2 = date1.find('div', {'class': 'display-name-date'})
            date3 = date2.find('span', {'class': 'review-date'})
            div8 = div7.find('div', {'class': 'text'})
            # self.log(div8.text)
            # self.log(date3.text)

            review_num = 'Review {0:0d}'.format(it_review)
            data_tmp = {}
            data_tmp['Date'] = date3.text
            data_tmp['Text'] = div8.text
            data[review_num] = data_tmp

            it_review += 1

        with open(filename, 'w') as f:
            json.dump(data, f)
        self.log('----------------------------------------')
