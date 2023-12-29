import bs4
import requests

from news import News

class NewsExtractor:
    def __init__(self):
        self.news_sources = {
            '9news.com.au': {
                'url': 'https://www.9news.com.au/uk',
                'news_div_selector': 'div.story__wrapper',
                'title_selector': 'h3',
                'annotation_selector': 'div.story__abstract',
                'date_selector': 'time'
            },
            'aljazeera.com': {
                'url': 'https://www.aljazeera.com/where/france/',
                'news_div_selector': 'div.gc__content',
                'title_selector': 'h3',
                'annotation_selector': 'div.gc__excerpt',
                'date_selector': 'div.date-simple span:nth-child(2)'
            },
            'japannews.yomiuri.co.jp': {
                'url': 'https://japannews.yomiuri.co.jp/latestnews/',
                'news_div_selector': 'li.clearfix',
                'title_selector': 'h2',
                'annotation_selector': 'h3',
                'date_selector': 'p'
            }
        }

    def get_news(self, source):
        if source in self.news_sources:
            news_list = []
            source_info = self.news_sources[source]
            url = source_info['url']
            html = requests.get(url).text
            soup = bs4.BeautifulSoup(html, features='html.parser')
            news_divs = soup.select(source_info['news_div_selector'])

            for div in news_divs:
                title = div.select_one(source_info['title_selector']).text.strip()
                description = ""
                try:
                    description = div.select_one(source_info['annotation_selector']).text.strip()
                except:
                    pass
                date = div.select_one(source_info['date_selector']).text.strip()
                resource = f"@{source}"

                news_list.append(
                    News(
                        title = title, 
                        date = date, 
                        description = description, 
                        resource = resource
                    )
                )
            return news_list
        else:
            return []

    def get_latest_news(self):
        latest_news_list = []
        for source in self.news_sources:
            news_list = self.get_news(source)
            latest_news_list.extend(news_list)
        return latest_news_list
    