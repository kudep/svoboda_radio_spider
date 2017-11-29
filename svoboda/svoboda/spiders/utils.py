# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
__all__ = ['get_links_from_html']

def get_links_from_html(src_html_file):
    '''
    src_html_file = 'Футурошок. Архив - Тексты.html'
    links = utils.get_links_from_html(src_html_file)
    '''
    with open(src_html_file) as file_desc:
        soup = BeautifulSoup(file_desc, "lxml")
    links = [x.get('href') for x in soup.findAll('a', {'class': 'img-wrap'})]
    return links
