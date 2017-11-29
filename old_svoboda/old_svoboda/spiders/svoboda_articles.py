# -*- coding: utf-8 -*-
import scrapy
import os, errno
import re

class SvobodaArticlesSpider(scrapy.Spider):
    name = 'svoboda_articles'
    # allowed_domains = ['archive.svoboda.org']
    start_urls = ['http://archive.svoboda.org/archive/']
    _base_folder ='/tmp/spider'#os.path.expanduser("~") + ''
    try:
        os.makedirs(_base_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    def parse(self, response):
        for program_href in response.css('tr>td>ul>li>a::attr(href)').extract():
            # url = response.urljoin(program_href)
            # self.log(url)
            yield response.follow(program_href, callback=self.programs_parse)

    def programs_parse(self, response):
        for topic_href in response.css('tr>td>p>a::attr(href)').extract():
            yield response.follow(topic_href, callback=self.topic_parse)

    def topic_parse(self, response):
        autors = []
        for autor in response.css('tr td p.person i b, tr td font p i b, tr td p i b').extract():
            if autor not in autors:
                autors.append(autor)
        filename = response.url.strip().split('/')[-1]
        path_to_file = os.path.join(self._base_folder, filename)
        replies = response.css('tr td p.person, tr td font p, tr td p').extract()
        replies = ''.join(replies)
        re
        if '<i><b>' in replies:
            replies = replies.strip().split('<i><b>')[1:]
        elif '<b><i>' in replies:
            replies = replies.strip().split('<b><i>')[1:]
        if len(replies) <= 1:
            self.log('warning')
            self.log(replies)
        else:
            self.log('info')
            self.log(replies)

        # with open(path_to_file,'wt') as file_desc:
        #     replies = response.css('tr td p.person, tr td font p, tr td p').extract():
        #         file_desc.write(replie + '\n'*3)
        self.log(len(autors))
        self.log(autors)
        if len(autors) == 0 :
            self.log(response.url)
            raise
