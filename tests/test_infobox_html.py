import pytest

from wiki_infobox_parser import infobox_html


@pytest.mark.parametrize('test_html, expected_html',
                         [
                             ('tests/test_files/test_infobox_page_2_en.html',
                              'tests/test_files/test_infobox_page_2_en_expected_no_css'),
                             ('tests/test_files/test_infobox_page_2_ru.html',
                              'tests/test_files/test_infobox_page_2_ru_expected_no_css'),
                             ('tests/test_files/test_infobox_page_1_en.html',
                              'tests/test_files/test_infobox_page_1_en_expected_no_css'),
                             ('tests/test_files/test_infobox_page_1_ru.html',
                              'tests/test_files/test_infobox_page_1_ru_expected_no_css'),
                         ]
                         )
def test_infobox_html_data(test_html, expected_html, monkeypatch):
    def mok_response(*args, **kwargs):
        with open(test_html, 'r', encoding='utf-8') as f:
            html = f.readlines()
        html = ''.join(html)
        return html

    with open(expected_html, 'r', encoding='utf-8') as f:
        expected_html_data = f.readlines()
    expected_html_data = ''.join(expected_html_data)

    monkeypatch.setattr('urllib.request.urlopen', mok_response)
    assert infobox_html('http://test') == expected_html_data
