# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import collections
import re
import os, errno

def get_links_from_html(src_html_file):
    '''
    src_html_file = 'Футурошок. Архив - Тексты.html'
    links = utils.get_links_from_html(src_html_file)
    '''
    with open(src_html_file) as file_desc:
        soup = BeautifulSoup(file_desc, "lxml")
    links = [x.get('href') for x in soup.findAll('a', {'class': 'img-wrap'})]
    return links


class FuturologySpider(scrapy.Spider):
    name = 'futurology'
    # allowed_domains = ['https://www.svoboda.org/z/17654']
    # start_urls = ['http://https://www.svoboda.org/z/17654/']
    src_html_file = 'spiders/Футурошок. Архив - Тексты.html'
    start_urls = get_links_from_html(src_html_file)
    _base_folder ='/tmp/spider'#os.path.expanduser("~") + ''
    try:
        os.makedirs(_base_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    def parse(self, response):
        page_id = response.url.split('/')[-2:]
        page_id = ''.join(page_id)
        path_to_file = os.path.join(self._base_folder, page_id)

        dirty_autors = response.css('div div div div div div div.wsw p em').extract()
        dirty_autors = list(map(lambda autor: BeautifulSoup(autor, "lxml").text.strip(), dirty_autors))
        dirty_autors = [autor for autor in dirty_autors if len(re.sub('[:\"\']', '', autor).strip()) > 1]
        autor_pattern = re.compile('[:\"\']')
        autors = map(lambda autor: re.sub('[:\"\']', '', autor).strip(), dirty_autors)
        dirty_autors = list(collections.OrderedDict.fromkeys(dirty_autors))
        autors = list(collections.OrderedDict.fromkeys(autors))

        autor_tags = {}
        for index, autor in enumerate(autors):
            autor_tags[autor] = '<'+str(index)+'>'
        dirty_autor_tags = {}
        for index, autor in enumerate(autors):
            dirty_autor_tags[autor] = autor_tags[re.sub('[:\"\']', '', autor).strip()]

        replies = response.css('div div div div div div div.wsw').extract_first()
        # self.log(dirty_autor_tags)
        # self.log(replies)
        replies = BeautifulSoup(replies, "lxml").text.strip()
        replies = re.sub('\n\n+.{1,250}\n\n+', '', replies)
        replies = re.sub('\n+', ' ', replies)
        for autor, tag in dirty_autor_tags.items():
             replies = re.sub(autor, tag, replies)
        replies = re.sub(r'(<\d+>)', r'\n\1', replies)
        replies = replies[1:] # deleted \n

        replies = re.sub(r'(<\d+>):', r'\1', replies)
        replies = re.sub('\u200b', '', replies)

        with open(path_to_file + '.meta', 'wt') as file_desc:
            file_desc.write('<url> '+ response.url+ '\n')
            for autor, tag in autor_tags.items():
                file_desc.write(tag + ' '+ autor + '\n')

        with open(path_to_file + '.data', 'wt') as file_desc:
            file_desc.write(replies)

        self.log(response.url+ ' is loaded.')
