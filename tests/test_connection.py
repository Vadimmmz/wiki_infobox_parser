from wiki_infobox_parser import connection
import pytest

page_html, page = connection('Дебюсси', 'ru')

def test_connection():
    assert type(page.title) == str and type(page_html) == str

