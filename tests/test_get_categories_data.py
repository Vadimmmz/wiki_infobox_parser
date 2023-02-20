import pytest
from wiki_infobox_parser import get_categories_data


result1_list = ['Централизованная библиотечная система города Ярославля',
                 'Ярославская областная универсальная научная библиотека имени Н. А. Некрасова']
result2_list = ['Частная библиотека', 'Валленродская библиотека', 'Библиотека герметической философии',
                'Библиотека Дидро', 'Лондонская библиотека', 'Библиотека Нью-Йоркского общества',
                'Патрацкая библиотека', 'Библиотека Пипса', 'Библиотека Прелингера', 'Библиотека Шейдов']

result3_list = ['Президентские библиотеки США', 'Президентская библиотека-музей Герберта Гувера',
                'Президентская библиотека-музей Джона Ф. Кеннеди', 'Президентский центр Клинтона',
                'Президентская библиотека Рональда Рейгана']

@pytest.mark.parametrize('path, result_list',
                         [
                             ('tests/test_files/test_category_libraries.html', result1_list),
                             ('tests/test_files/test_category_private_libraries.html', result2_list),
                             ('tests/test_files/test_category_president_libraries.html', result3_list)
                          ]
                         )
def test_get_categories_data(path, result_list, monkeypatch):

    def mok_response(*args, **kwargs):

        with open(path, 'r', encoding='utf-8') as f:
            html = f.readlines()
        html = ''.join(html)
        return html

    monkeypatch.setattr('urllib.request.urlopen', mok_response)
    assert get_categories_data('http://test') == result_list



