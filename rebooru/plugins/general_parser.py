import os
from urllib.parse import urlparse

from yapsy.IPlugin import IPlugin
from bs4 import BeautifulSoup
import requests

from rebooru.models import ParseResult

class ParserPlugin(IPlugin):
    def parse_url(self, url):
        source_url = url
        html_soup = BeautifulSoup(requests.get(url).content, "html.parser")
        tag_hrefs = []
        for a_tag in html_soup.select('a'):
            href = a_tag.attrs.get('href', None)
            if a_tag.select('img') and href is not None:
                tag_hrefs.append(href)
        for href in tag_hrefs:
            url = href
            if href.startswith('/'):
                url = urljoin(url, href)
            splitted_path = os.path.splitext(urlparse(url).path)
            ext = splitted_path[1] if len(splitted_path) > 1 else None
            if ext.lower() in ('.jpg', '.jpeg', '.png'):
                url_type = ParseResult.TYPE_IMAGE
            else:
                url_type = ParseResult.TYPE_PAGE
            yield {
                'url': url,
                'type': url_type,
                "source_url": source_url,
            }
