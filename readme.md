# Wiki infobox parser

The wiki infobox parser is designed for parsing infobox menu data from the site wikipedia.org.
With this module, you can easily extract both all data and sample values. 
This module allows you to extract data in text format or in the form of html code,
as well as, if necessary, create files with the received data. With a few simple actions, 
we can get data from thousands of pages in a very short time.

## Used packages

- beautifulsoup4~=4.11.1

## How to use
Read this instruction once and you will have no questions about how 
to use this module. The text below describes the operation of the main 
functions of the program and examples of their use. I hope this module
will be useful for you.

### infobox_text() function 
let's take a quick look for work with this module.
Imagine that we need to quickly get information about some person or something else,
from wikipedia infobox tables an article about which is (or maybe is) in Wikipedia.

```python
data = infobox_text('Fyodor Dostoevsky')
print(data)
```

As we can see, the function returns information from the information 
block in the form of a ***{key:value}*** dictionary

This module provide properly works for **russian** and **english** languages.
Default language is english, and if you want search something in russian wiki
you should set attribute ***lang='ru'***

```python
data = infobox_text('Федор Достоевский', lang='ru')
print(data)
```


We also can use URL instead text requests. In that way parser will work more
quickly.

If you use URL then it doesn't necessity to set ***lang*** 
attribute.
```python
url = 'https://en.wikipedia.org/wiki/Fyodor_Dostoevsky'
data = infobox_text(url)
print(data)
```

In case when we want to find just information about exactly menu items,
and don't want any different information from this artickle infobox we can 
pass the list to the place of the second attribute. 
The list will contain the items of the infobox table that we want to get. 
(If they happen to be there)

At first let's create list that will consist neccesary items and put it
in the second attrubute **infobox_text()**

```python
menu_words = ['Born', 'Died', 'Years active']

# just put the list in second parameter place
data = infobox_text('Fyodor Dostoevsky', menu_words)

# or use named parameter 'items'
data = infobox_text('Fyodor Dostoevsky', items=menu_words)
print(data)

# We also can use URL, and it's a preferable way to use this function
# Because it works too faster, than without URLs using

url = 'https://en.wikipedia.org/wiki/Fyodor_Dostoevsky'
data = infobox_text(url, menu_words)
print(data)

```
This will be the result of executing this code:
```python
# {
# 'title': 'Fyodor Dostoevsky', 'Born': 'Fyodor Mikhailovich Dostoevsky
#          ( 1821-11-11 ) 11 November 1821 Moscow , Moskovsky Uyezd , 
#           Moscow Governorate , Russian Empire', 
#
# 'Died': '28 January 1881 (1881-01-28) (aged 59) Saint Petersburg ,
#          Saint Petersburg Governorate , Russian Empire', 
#
# 'Years active': '1844–1880'
# }
```

We can display the results of the query on the screen without resorting 
to the print() function, for this we need to specify the **print_result=True** 
attribute:

```python
infobox_text(url, menu_words, print_result=True)
```

Result will look like that:

```python
# title : Fyodor Dostoevsky
# Born : Fyodor Mikhailovich Dostoevsky ( 1821-11-11 ) 11 November 1821 Moscow , Moskovsky Uyezd , Moscow Governorate , Russian Empire
# Died : 28 January 1881 (1881-01-28) (aged 59) Saint Petersburg , Saint Petersburg Governorate , Russian Empire
# Years active : 1844–1880
```
If we want to get information about several people, we need 
to create a list with names and iterate through this list:
```python
names = ['Erich Remarque', 'Vladimir Nabokov', 'Fyodor Dostoevsky']
for i in names:
    infobox_text(i, menu_words, print_result=True)

```
To get all infomation about the writers just don't set second parameter. 
In that case you will get all items from page's infobox.
```python
names = ['Erich Remarque', 'Vladimir Nabokov', 'Fyodor Dostoevsky']
for i in names:
    infobox_text(i, print_result=True)
```
After executing the request, we will get this result. Note that 
only the last writer has "Years active" item. 
It happened becausse only this writer had such an item on his page in the 
infobox table.

```python
# title : Erich Maria Remarque
# Born : Erich Paul Remark ( 1898-06-22 ) 22 June 1898 Osnabrück , Kingdom of Prussia , German Empire
# Died : 25 September 1970 (1970-09-25) (aged 72) Locarno , Switzerland
#
# title : Vladimir Nabokov
# Born : 22 April O.S. 10 1899 a] Saint Petersburg , Russian Empire
# Died : 2 July 1977 (1977-07-02) (aged 78) Montreux , Switzerland
#
# title : Fyodor Dostoevsky
# Born : Fyodor Mikhailovich Dostoevsky ( 1821-11-11 ) 11 November 1821 Moscow , Moskovsky Uyezd , Moscow Governorate , Russian Empire
# Died : 28 January 1881 (1881-01-28) (aged 59) Saint Petersburg , Saint Petersburg Governorate , Russian Empire
# Years active : 1844–1880
```
### get_categories_data() function 

The get_categories_data() function allows us to get a list of all entries in 
Wikipedia sections of the "Category" type. Let's see how this can be 
useful to get the necessary data from the infobox tables

Make variable which will contained URL for some "category" type wikipedia page.
```python
url_drummers = "https://en.wikipedia.org/wiki/Category:21st-century_American_drummers"

list_drummers = get_categories_data(url_drummers)
print(list_drummers)

# If we can see numbers of values in list if show_len=True
list_drummers = get_categories_data(url_drummers, show_len=True)
print(list_drummers)
```
If we specify the parameter href_dict=True, 
the function returns not a list, but a list with dictionaries. This list has the following structure:
**[{'title': Article title, 'url': article URL}]**

```python
list_drummers = get_categories_data(url_drummers, show_len=True)
print(list_drummers)
```

Now, we can find the records we are interested in for each record in the resulting sheet using the infobox_text() function
The speed of parsing increases several times if you use iteration by URL, and not by text values
```python
url_drummers = "https://en.wikipedia.org/wiki/Category:21st-century_American_drummers"
list_drummers = get_categories_data(url_drummers, show_len=True)

# Imagine that we want get just this values for each element in list_drummers
list_with_keywords = ['Birth name','Born','Genres','Groups','Years active','labels']

#Pay attention on "i" variable. That we will use URLs only
for i in list_drummers:
    infobox_text(i['url'], list_with_keywords, print_result=True)
```
In the following example, we will disable the print_result parameter and display 
the values on the screen during the iteration. In this way we can use the received data,
for example, write them to a database or a text file.

```python
for i in list_drummers:
    # let's display the information on the screen in a different way
    # Note that when we iterate over the url, we don't need to set a value for the 'lang' parameter
    data = infobox_text(i['url'], list_with_keywords)

    for i in data.keys():
        print(f"{i} : {data[i]}")
    else:
        print("\n")
```

Example of writing to a file using the **write_to_file()** function. This is a very simple
function that adds the resulting value to the file. It should be remembered 
that the function does not overwrite the file, but adds the resulting value to 
it at each iteration. The function has only two parameters 'data' and 'file_name'.

```python
for i in list_drummers:
    data = infobox_text(i['url'], list_with_keywords, print_result=True)

    for i in data.keys():
        write_to_file(f"{i} : {data[i]}\n", 'example_file.txt')
    else:
        write_to_file("\n\n", 'example_file.txt')
```
Entries for pages that do not have an infobox table will look like this.
```commandline
error : ('https://en.wikipedia.org/wiki/Alex_Bailey_(musician)', Exception('There is not infobox in this article'))
```
In the last example, let's consider one of the options for how you can record all such records in a separate file and not include them in the file
with correct data

```python
for i in list_drummers:

    data = infobox_text(i['url'], list_with_keywords , print_result=True)

    for i in data.keys():
        # sing the 'error' key, we can track all articles that do not have
        # an infobox table and write them to a separate file
        if i == 'error':
            write_to_file(f"{i} : {data[i]}\n", 'errors.txt')
        else:
            write_to_file(f"{i} : {data[i]}\n", 'drummers.txt')

    write_to_file("\n\n", 'drummers.txt')
```

### infoblock_html function

We pass the value of 'Fyodor Dostoevsky' to the search parameter to get the html code of the infoblock.
The function returns the html code of the infoblock of a given page as a string.

```python
print(infobox_html('Fyodor Dostoevsky'))
```
To search in the Russian Wikipedia, you need to set the value of the parameter ***lang='ru'***

```python
print(infobox_html('Дебюсси', lang='ru'))
```

The value of the ***create_html=True*** attribute will create html file wiki_infobox.html

```python
print(infobox_html('Fyodor Dostoevsky', create_html=True))
```
We can set a name for the file being created using the ***'file_name'*** attribute
```python
print(infobox_html('Fyodor Dostoevsky', create_html=True, file_name='Fyodor Dostoevsky.html'))
```

As in all other cases, when we use a URL instead of a text request, we do not need to set values 
for the 'lang' parameter and the speed of the function execution will be much faster.
```python
url = "https://es.wikipedia.org/wiki/Fi%C3%B3dor_Dostoyevski"
print(infobox_html(url, create_html=True, file_name='from_url.html'))
```
## About exceptions and errors

When using the **infobox_text()** function, there are two main types of exceptions. 
The first type of exception is a regular situation when there is no infobox table on the page .
The second type is an incorrect query or the query that is ambiguous for wikipedia search. 
For example, we will enter the query *'John smith'*.
```python
print(infobox_text('John Smith'))
```
In the dictionary, which we will get will
be a single key *'error'*, which will contain both the query itself and the error description. 
This is because a huge number of pages can refer to the query 'John Smith' by software. 
To exclude such situations, formulate the request as accurately as possible, for example:
```python
print(infobox_text('John Smith flying ace'))
```
This type of exception occurs exclusively when you use a text query.
This type of error is not possible when using a URL.

## Liense

MIT License