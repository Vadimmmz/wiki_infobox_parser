from wiki_infobox_parser import infobox_text
import pytest

dicts_without_attribute_using = [
    {'title': 'Fyodor Dostoevsky', 'Born': 'Fyodor Mikhailovich Dostoevsky ( 1821-11-11 ) 11 November 1821 Moscow ,'
                                           ' Moskovsky Uyezd , Moscow Governorate , Russian Empire',
     'Died': '9 February 1881 (1881-02-09) (aged 59) Saint Petersburg , Saint Petersburg Governorate , Russian Empire',
     'Occupation': 'Military engineer novelist journalist', 'Education': 'Military Engineering-Technical University',
     'Genre': 'Novel short story journalism', 'Literary movement': 'Realism , Philosophy , Personality psychology',
     'Years active': '1844–1880',
     'Notable works': 'Notes from Underground (1864) Crime and Punishment (1866) The Idiot (1868–1869) '
                      'Demons (1871–1872) The Brothers Karamazov (1879–1880)',
     'Spouse': 'Maria Dmitriyevna Isaeva  ( m. 1857 ; died 1864 ) Anna Grigoryevna Snitkina  ( m. 1867 ) ',
     'Children': '4, including Lyubov Dostoevskaya'},

    {'title': 'Фёдор Михайлович Достоевский',
     'Псевдонимы': 'Д.; Друг Козьмы Пруткова; Зубоскал; —ий, М.; Летописец; М-ий; Н. Н.; '
                   'Пружинин, Зубоскалов, Белопяткин и К° Ред.; Ф. Д.; N.N. ',
     'Дата рождения': '30 октября 11 ноября 1821',
     'Место рождения': 'Москва , Российская империя',
     'Дата смерти': '28 января 9 февраля 1881', 'Место смерти': 'Санкт-Петербург , Российская империя',
     'Гражданство (подданство)': 'Российская империя', 'Род деятельности': 'прозаик , переводчик , философ',
     'Годы творчества': '1844 — 1880', 'Направление': 'реализм', 'Язык произведений': 'русский',
     'Автограф': 'Изображение автографа'},

    {'title': 'Ella Fitzgerald',
     'Born': 'Ella Jane Fitzgerald ( 1917-04-25 ) April 25, 1917 Newport News, Virginia , U.S.',
     'Died': 'June 15, 1996 (1996-06-15) (aged 79) Beverly Hills, California , U.S.',
     'Resting place': 'Inglewood Park Cemetery', 'Occupation': 'Singer',
     'Spouses': 'Benny Kornegay  ( m. 1941; annulled 1942) Ray Brown  ( m. 1947; div. 1953) ',
     'Children': 'Ray Brown Jr.',
     'Genres': 'Jazz swing bebop traditional pop blues soul doo-wop post-bop rock and roll',
     'Instrument(s)': 'Vocals', 'Years active': '1929–1995', 'Labels': 'Decca Verve Capitol Reprise Pablo',
     'Website': 'ellafitzgerald .com'},

    {'title': 'Элла Фицджеральд', 'Имя при рождении': 'англ. Ella Jane Fitzgerald',
     'Полное имя': 'Элла Джейн Фицджеральд', 'Дата рождения': '25 апреля 1917 ( 1917-04-25 )',
     'Место рождения': 'Ньюпорт-Ньюс , Виргиния , США', 'Дата смерти': '15 июня 1996 ( 1996-06-15 ) (79 лет)',
     'Место смерти': 'Беверли-Хиллз , Калифорния , США', 'Похоронена': 'Инглвуд-Парк', 'Страна': 'США',
     'Профессии': 'певица', 'Годы активности': '1934—1993', 'Певческий голос': 'меццо-сопрано',
     'Инструменты': 'фортепиано', 'Жанры': 'Джаз , свинг , традиционная поп-музыка',
     'Псевдонимы': '«Леди Элла», «Первая леди джаза»', 'Лейблы': 'Decca Records , Verve Records',
     'Награды': 'Presidential Medal of Freedom (ribbon), Order of the Eagle of Georgia - ribbon bar,'
                ' Кавалер ордена Искусств и литературы (Франция), Kennedy Center Ribbon'}
]

dicts_with_items = [
    {'title': 'Fyodor Dostoevsky', 'Born': 'Fyodor Mikhailovich Dostoevsky ( 1821-11-11 ) 11 November 1821 Moscow ,'
                                           ' Moskovsky Uyezd , Moscow Governorate , Russian Empire',
     'Died': '9 February 1881 (1881-02-09) (aged 59) Saint Petersburg , Saint Petersburg Governorate , Russian Empire'
     },

    {'title': 'Фёдор Михайлович Достоевский',
     'Дата рождения': '30 октября 11 ноября 1821',
     'Дата смерти': '28 января 9 февраля 1881'},

    {'title': 'Ella Fitzgerald',
     'Born': 'Ella Jane Fitzgerald ( 1917-04-25 ) April 25, 1917 Newport News, Virginia , U.S.',
     'Died': 'June 15, 1996 (1996-06-15) (aged 79) Beverly Hills, California , U.S.'},

    {'title': 'Элла Фицджеральд', 'Дата рождения': '25 апреля 1917 ( 1917-04-25 )',
     'Дата смерти': '15 июня 1996 ( 1996-06-15 ) (79 лет)'}
]

dicts_with_items_and_url = [
    {'title': 'Fyodor Dostoevsky', 'Born': 'Fyodor Mikhailovich Dostoevsky ( 1821-11-11 ) 11 November 1821 Moscow ,'
                                           ' Moskovsky Uyezd , Moscow Governorate , Russian Empire',
     'Died': '9 February 1881 (1881-02-09) (aged 59) Saint Petersburg , Saint Petersburg Governorate , Russian Empire',
     'url': 'http://test'
     },

    {'title': 'Фёдор Михайлович Достоевский',
     'Дата рождения': '30 октября 11 ноября 1821',
     'Дата смерти': '28 января 9 февраля 1881',
     'url': 'http://test'},

    {'title': 'Ella Fitzgerald',
     'Born': 'Ella Jane Fitzgerald ( 1917-04-25 ) April 25, 1917 Newport News, Virginia , U.S.',
     'Died': 'June 15, 1996 (1996-06-15) (aged 79) Beverly Hills, California , U.S.',
     'url': 'http://test'},

    {'title': 'Элла Фицджеральд', 'Дата рождения': '25 апреля 1917 ( 1917-04-25 )',
     'Дата смерти': '15 июня 1996 ( 1996-06-15 ) (79 лет)',
     'url': 'http://test'}
]

test_items = ['born', 'died', 'дата рождения', 'дата смерти']


@pytest.mark.parametrize('test_html, expected_result',
                         [
                             ('tests/test_files/test_infobox_page_1_en.html',
                              dicts_without_attribute_using[0]),
                             ('tests/test_files/test_infobox_page_1_ru.html',
                              dicts_without_attribute_using[1]),
                             ('tests/test_files/test_infobox_page_2_en.html',
                              dicts_without_attribute_using[2]),
                             ('tests/test_files/test_infobox_page_2_ru.html',
                              dicts_without_attribute_using[3])
                         ]
                         )
def test_infobox_text(test_html, expected_result, monkeypatch):
    def mok_response(*args, **kwargs):
        with open(test_html, 'r', encoding='utf-8') as f:
            html = f.readlines()
        html = ''.join(html)
        return html

    monkeypatch.setattr('urllib.request.urlopen', mok_response)
    assert infobox_text('http://test') == expected_result


@pytest.mark.parametrize('test_html, expected_result',
                         [
                             ('tests/test_files/test_infobox_page_1_en.html',
                              dicts_with_items[0]),
                             ('tests/test_files/test_infobox_page_1_ru.html',
                              dicts_with_items[1]),
                             ('tests/test_files/test_infobox_page_2_en.html',
                              dicts_with_items[2]),
                             ('tests/test_files/test_infobox_page_2_ru.html',
                              dicts_with_items[3])
                         ]
                         )
def test_infobox_text_items_using(test_html, expected_result, monkeypatch):
    def mok_response(*args, **kwargs):
        with open(test_html, 'r', encoding='utf-8') as f:
            html = f.readlines()
        html = ''.join(html)
        return html

    monkeypatch.setattr('urllib.request.urlopen', mok_response)
    assert infobox_text('http://test', items=test_items) == expected_result


@pytest.mark.parametrize('test_html, expected_result',
                         [
                             ('tests/test_files/test_infobox_page_1_en.html',
                              dicts_with_items_and_url[0]),
                             ('tests/test_files/test_infobox_page_1_ru.html',
                              dicts_with_items_and_url[1]),
                             ('tests/test_files/test_infobox_page_2_en.html',
                              dicts_with_items_and_url[2]),
                             ('tests/test_files/test_infobox_page_2_ru.html',
                              dicts_with_items_and_url[3])
                         ]
                         )
def test_infobox_text_items_and_gethref_using(test_html, expected_result, monkeypatch):
    def mok_response(*args, **kwargs):
        with open(test_html, 'r', encoding='utf-8') as f:
            html = f.readlines()
        html = ''.join(html)
        return html

    monkeypatch.setattr('urllib.request.urlopen', mok_response)
    assert infobox_text('http://test', items=test_items, get_url=True) == expected_result
