import re

from declare import Field, Item, MapField, prepare, MAGIC as S

import requests
from bs4 import BeautifulSoup


class Torrent(Item):
    @prepare
    def prep(self, soup):
        cats, links, seeders, leechers = soup.findAll('td')
        soup._links = links.findAll('a')

        soup._match = re.search('Uploaded (.*), Size (.*), ULed by (.*)',
                                links.find('font').get_text()).groups(0)

        soup._seeders = seeders.get_text()
        soup._leechers = leechers.get_text()

    name = S._links[0].get_text()
    link = S._links[0]['href']
    magnet = S._links[1]['href']

    @Field
    def torrent(soup):
        try:
            return soup._links[2]['href']
        except IndexError:
            return None

    created = S._match[0]
    size = S._match[1]
    user = S._match[2]

    seeders = Field(lambda s: int(s._seeders))
    leechers = Field(lambda s: int(s._leechers))


class Page(Item):
    torrents = MapField(Torrent, S.find(['table']).findAll('tr')[1:-1])


def search(query):
    url = 'http://thepiratebay.sx/search/{}'.format(query)
    s = BeautifulSoup(requests.get(url).text)
    p = Page(s)
    return p.torrents


if __name__ == '__main__':
    for t in search('mad men'):
        print(t.name)
