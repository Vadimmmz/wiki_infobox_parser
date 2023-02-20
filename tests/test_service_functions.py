from wiki_infobox_parser import lang_definer, text_cleaner, is_https
import pytest

lang_definer_list = [
    ("https://ru.wikipedia.org/wiki/%D0%9D%D1%8C%D1%8E-%D0%99%D0%BE%D1%80%D0%BA", 'ru'),
    ("https://got.wikipedia.org/wiki", 'got'),
    ("https://simple.wikipedia.org/wiki/County_seat", 'simple')
]


@pytest.mark.parametrize("url, expected_result", lang_definer_list)
def test_lang_definer_good(url, expected_result):
    assert lang_definer(url) == expected_result, "Language detection doesn't work properly"


bad_urls = [
    "https:/got.wikipedia.org/wiki",
    "https//simple.wikipedia.org/wiki/County_seat",
    "fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal",
    "Test text",
    "One more test text"
]


@pytest.mark.parametrize("url", bad_urls)
def test_lang_definer_bad(url):
    with pytest.raises(IndexError):
        lang_definer(url)


good_urls = [
    "https://ru.wikipedia.org/wiki/%D0%9D%D1%8C%D1%8E-%D0%99%D0%BE%D1%80%D0%BA",
    "https://got.wikipedia.org/wiki",
    "https://simple.wikipedia.org/wiki/County_seat"
]


@pytest.mark.parametrize("url", good_urls)
def test_is_http_good(url):
    assert is_https(url) is True


@pytest.mark.parametrize("url", bad_urls)
def test_is_http_bad(url):
    assert is_https(url) is False


text_cleaner_list = [
    ("Some [1] text", "Some text"),
    ("Some [1][2] text", "Some text"),
    ("Some\u200b text", "Some text"),
    ("Some\xa0 text", "Some text"),
    ("Some  text", "Some text")
]


@pytest.mark.parametrize("text_before, text_after", text_cleaner_list)
def test_text_cleaner_good(text_before, text_after):
    assert text_cleaner(text_before) == text_after




