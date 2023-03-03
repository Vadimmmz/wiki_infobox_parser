from wiki_infobox_parser import connection
import pytest
import urllib.request

page_html, page_url = connection('Дебюсси', 'ru')


def test_connection():
    assert type(page_url) == str and type(page_html) == type(urllib.request.urlopen('http://en.wikipedia.com'))
