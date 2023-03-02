import wikipedia
from bs4 import BeautifulSoup
import urllib.request
import re
from typing import Optional


def write_to_file(data: str, file_name: str):
    path = file_name
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(data)


def lang_definer(url: str) -> str:
    match = re.findall(r"://\w+", url)
    lang = match[0][3:]
    return lang


def text_cleaner(value: str) -> str:
    list_for_remove = []
    result_4_compare = value.split(" ")
    for i in result_4_compare:
        if "[" in i or "]" in i:
            list_for_remove.append(i)
    for i in list_for_remove:
        value = value.replace(i, '')
        value = value.replace('  ', ' ')
    value = value.replace(u'\u200b', '')
    value = value.replace(u'\xa0', ' ')
    value = value.replace('  ', ' ')
    return value


def is_https(search: str) -> bool:
    """ This function is checking if input value is url """

    if search.startswith(("https://", "http://")):
        return True
    else:
        return False


def connection(search: str, lang: str) -> tuple:
    # Checking if input values is url
    if is_https(search):
        page_html: str = urllib.request.urlopen(search)
        page = None
    else:
        #https://ru.wikipedia.org/w/api.php?action=opensearch&format=json&search=SEARCHREQUESTPUTHERE&namespace=0&limit=10&formatversion=2
        wikipedia.set_lang(lang)
        search_result: list = wikipedia.search(search)

        page = wikipedia.page(search_result[0], auto_suggest=False)
        page_html: str = page.html()
    return page_html, page


# *** How to annotate BS4 object?? ***
def infobox_item(items: list, soup) -> dict:
    result_dict = dict()

    # Making the first variable 'title' entry in the dict
    th_text = soup.find('table', class_='infobox').find('th', class_='infobox-above')
    if th_text is not None:
        th_text = th_text.text
        text = th_text.strip().replace(u'\xa0', u' ')
        result_dict['title'] = text

    th_text = soup.find('table', class_='infobox').find_all('th')

    # Items list format
    req_list_to_compare = []
    for i in items:
        i = i.lower()
        req_list_to_compare.append(i)

    for i in th_text:
        # Set values format to comparing with request
        i_format = str(i.text)
        i_format = i_format.lower().strip().replace(u'\xa0', u' ')

        if i_format in req_list_to_compare:

            text = i.text.strip().replace(u'\xa0', u' ')
            data = i.findNext('td').get_text(strip=True, separator=' ')
            data = data.replace(u'\xa0', u' ')

            # If data value have no text, but have any images if it is here
            data_empty = i.findNext('td').find_all('img', alt=True)

            if data_empty and not data:
                for i in data_empty:
                    # If is '.jpg' or somthing like it in name then remove it
                    alt_checking = i['alt'].strip()

                    if alt_checking[-4] == '.':
                        data += alt_checking[:-4] + ", "
                    else:
                        data += alt_checking + ", "
                else:
                    # Remove ',' from the end of the string
                    data = data[:-2]

            # Remove all wiki links with help remover_remover()
            result_dict[text] = text_cleaner(data)

    return result_dict


# ho to annotate?
# <class 'wikipedia.wikipedia.WikipediaPage'>
# and this
# <class 'bs4.BeautifulSoup'>
def infobox_all(search: str, soup, page, summary: bool = False) -> dict:

    result_dict = dict()
    tr = soup.find('table', class_='infobox').find_all('tr')

    # If attribute 'summary' is True
    if summary:
        if not is_https(search):
            data = page.summary + '\n' * 2
            # Atrticle's summary will stored with keyname 'summary''
            result_dict['summary'] = text_cleaner(data)

    key_for_dict = None

    for i in tr:
        # Finding all th tags
        th = i.find('th')

        if th is not None:
            th = i.find('th', class_=['infobox-above'])

            if th is not None:
                # The title of the article will store with keyname 'title'
                result_dict['title'] = th.text.strip()
                continue

            else:
                th = i.find('th', class_=['infobox-header'])
                if th is not None:
                    # There's possible to get infobox-hearder's text. Just add to result_dict
                    # value from th.text
                    pass
                else:
                    th = i.find('th')
                    key_for_dict = text_cleaner(th.text)
        else:
            continue

        td = i.find('td')

        if td is not None:
            td = i.find('td', class_=['infobox-below'])
            if td is not None:
                # There's possible to get infobox-below's text. Just add to result_dict
                # value from td.text
                continue
            else:
                td = i.find('td').get_text(strip=True, separator=' ')
                td = "".join(td)
                data = td.strip()

                if key_for_dict is not None:
                    result_dict[key_for_dict] = text_cleaner(data)

                if data == '':

                    # If here is not any text, but here is images then taking just alt text from images
                    data_empty = i.find('td').find_all('img', alt=True)
                    if data_empty:
                        for i in data_empty:
                            # If is '.jpg' or somthing like it in name then remove it
                            alt_checking = i['alt'].strip()

                            if alt_checking[-4] == '.':
                                data += alt_checking[:-4] + ", "
                            else:
                                data += alt_checking + ", "
                        else:
                            # Remove ',' from the end of the string
                            data = data[:-2]
                            result_dict[key_for_dict] = text_cleaner(data)
    return result_dict


def infobox_text(search: str, items: Optional[list] = None,
                 lang: str = 'en', print_result: bool = False,
                 get_url: bool = False, summary: bool = False):
    try:
        page_html, page = connection(search, lang)
        soup = BeautifulSoup(page_html, 'lxml')

        # Get article's infobox header, and write it in result dictionary
        check_if_infobox = soup.find('table', class_='infobox')

        # If article have not infobox then raise exception
        if check_if_infobox is None:
            raise Exception('There is not infobox in this article')

    except Exception as e:

        result_dict = dict()
        result_dict['error'] = search, e
        return result_dict

    if items is not None:
        result_dict = infobox_item(items=items, soup=soup)
    else:
        result_dict = infobox_all(search=search, soup=soup, page=page, summary=summary)

    # add url for each wiki page in result if attribute get_url is True:
    if get_url:
        if is_https(search):
            result_dict['url'] = search
        else:
            result_dict['url'] = page.url

    # print result if "print" parameter is True
    if print_result:
        if len(result_dict.keys()) > 1:
            for i in result_dict.keys():
                print(f"{i} : {result_dict[i]}")
            else:
                print("\n")

    return result_dict


def infobox_html(search: str, create_html: bool = False,
                 lang: str = 'en', file_name: Optional[str] = None) -> str:

    if is_https(search):
        lang = lang_definer(search)

    try:
        page_html, page = connection(search, lang)
        soup = BeautifulSoup(page_html, 'lxml')

        # Get article's infobox header, and write it in result dictionary
        check_if_infobox = soup.find('table', class_='infobox')

        # If article have not infobox then raise exception
        if check_if_infobox is None:
            raise Exception('There is not infobox in this article')

    except Exception as e:
        result = f'Error: {e}'
        return result

    # Write html in file
    if create_html:

        # Check if file_name attribute was received
        if file_name is None:
            file_name = 'wiki_infobox_data.html'

        with open('style.css', 'r') as f:
            css = f.readlines()
        css = " ".join(css)

        result = '<html><head><meta charset="utf-8">' \
                 f'<style>{css}</style>' \
                 '</head><body>' + str(check_if_infobox) + '</body></html>'

        with open(file_name, 'w', -1, 'UTF8') as f:
            f.write(result)

    result = str(check_if_infobox)

    return result


def get_categories_data(url: str, show_len: bool = False, href_dict: bool = False) -> list:
    data = []
    next_page_title = ['next page', 'Следующая страница']

    try:
        # Checking if url is correct
        if not is_https(url):
            raise Exception('Incorrect url')
        # Language definition
        lang = lang_definer(url)

        url_html = urllib.request.urlopen(url)
        soup = BeautifulSoup(url_html, 'lxml')
        th_text = soup.find('div', class_='mw-content-ltr').find_all('li')

    except Exception as e:
        data = [e]
        return data

    for i in th_text:

        i = i.find('a', title=True)
        if i is not None:
            if i['title'][:9] not in ['q:Категор', 'Категория', 'commons:C', 'Category:']:
                if href_dict:
                    url = 'https://' + lang + '.wikipedia.org' + i['href']
                    data.append({'title': i['title'], 'url': url})
                else:
                    data.append(i['title'])

    next_url = soup.find('div', class_='mw-content-ltr').find_all('a')
    for i in next_url:
        if i.text in next_page_title:
            url = 'https://' + lang + '.wikipedia.org' + i['href']

            next_page_data = get_categories_data(url, href_dict=href_dict)
            data.extend(next_page_data)
            break

    if show_len:
        print(f"Number of values found: {len(data)}")

    return data
