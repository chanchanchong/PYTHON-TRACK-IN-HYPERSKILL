# Beautiful Soup Documentation
# Beautiful Soup is a Python library for pulling data out of
# HTML and XML files. It works with your favorite parser to
# provide idiomatic ways of navigating, searching , and
# modifying the parse tree. It commonly saves programmers hours
# or days of work.

# These instructions illustrate all major features of Beautiful
# Soup 4, with examples. I'll show you what the library is good for,
# how it works, how to use it,
# how to make it do what you want, and what to do when it
# violates your expectations.

# This document covers Beautiful Soup version 4.9.3. The
# examples in this documentation should work the same way in
# Python 2.7 and Python 3.8.

# You might be looking for the documentation for Beautiful Soup
# 3. If so, you should know that Beautiful Soup 3 is no longer
# being developed and that support for it will be dropped on or
# after December 31, 2020. If you want to learn about the
# differences between Beautiful Soup 3 and Beautiful Soup 4,
# see Porting code to BS4.

# Quick Start
# Here's an HTML document I'll be using as an example
# throughout this document. It's part of a story from Alice in
# Wonderland.

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# Running the "three sisters" document through Beautiful Soup 
# gives us a BeautifulSoup object, which represents the document 
# as a nested data structure:

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())

# Here are some simple ways to navigate that data structure:
# print(soup.title)
# <title>The Dormouse's story</title>

# print(soup.title.name)
# title

# print(soup.title.string)
# The Dormouse's story

# print(soup.title.parent.name)
# head

# print(soup.p)
# <p class="title"><b>The Dormouse's story</b></p>

# print(soup.p['class'])
# ['title']

# print(soup.a)
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>

# print(soup.find_all('a'))
# # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# #  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
# #  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# print(soup.find(id="link3"))
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

# One common task is extracting all the URLs found within a
# page's <a> tags:
# for link in soup.find_all('a'):
#     print(link.get('href'))
# http://example.com/elsie
# http://example.com/lacie
# http://example.com/tillie

# Another common task is extracting all the text from a page:
# print(soup.get_text())
# The Dormouse's story
#
# The Dormouse's story
#
# Once upon a time there were three little sisters; and their names were
# Elsie,
# Lacie and
# Tillie;
# and they lived at the bottom of a well.
#
# ...

# Kinds of objects
# Beautiful Soup transforms a complex HTML document into a
# complex tree of Python objects. But you'll only ever have to
# deal with about four kinds of objects: Tag, NavigableString,
# BeautifulSoup, and Comment.

# Tag
# A Tag object corresponds to an XML or HTML tag in the original
# document:
# soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
# tag = soup.b
# print(type(tag))

# Tags have a lot of attributes and methods, and I'll cover most of
# them in Navigating the tree and Search the tree. For now,
# the most important features of a tag are its name and
# attributes.

# Name
# Every tag has a name, accessible as .name:
# print(tag.name)
# b

# If you change a tag's name, the change will be reflected in any
# HTML markup generated by Beautiful Soup:
# tag.name = "blockquote"
# print(tag)
# <blockquote class="boldest">Extremely bold</blockquote>

# Attributes
# A tag may have any number of attributes. The tag <b
# id="boldest"> has an attribute "id" whose value is "boldest". You
# can access a tag's attributes by treaing the tag like a
# dictionary:
# print(tag['id'])
# boldest

# You can access that directly as .attrs:
# print(tag.attrs)
# {'id': 'boldest'}

# You can add, remove and modify a tag's attributes. Again, this
# is one by treating the tag as a dictionary:
# tag['id'] = 'verybold'
# tag['another-attribute'] = 1
# print(tag)
# <b another-attribute="1" id="verybold"></b>

# del tag['id']
# del tag['another-attribute']
# print(tag)

# print(tag['id'])
# KeyError: 'id'
# print(tag.get('id'))
# None

# Multi-valued attributes
# HTML 4 defines a few attributes that can have multiple values.
# HTML 5 removes a couple of them, but defines a few more.
# The most common multi-valued attribute is class (that is, a tag
# can have more than one CSS class). Others include rel, rev,
# accept-charset, headers, and accesskey. Beautiful Soup presents
# the value(s) of a multi-valued attribute as a list:
# css_soup = BeautifulSoup('<p class="body"></p>', 'html.parser')
# print(css_soup.p['class'])
# ['body']

# css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
# print(css_soup.p['class'])
# ['body', 'strikeout']

# If an attribute looks like it has more than one value, but it's not
# a multi-valued attribute as defined by any version of the HTML
# standard, Beautiful Soup will leave the attribute alone:
# id_soup = BeautifulSoup('<p id="my id"></p>', 'html.parser')
# print(id_soup.p['id'])
# 'my id'

# When you turn a tag back into a string, multiple attribute values
# are consolidated:
# rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>', 'html.parser')
# print(rel_soup.a['rel'])

anchor = """<a href="/translation/french-english/bonjour" class="translation ltr dict adv" data-pos="[adv]" data-pos-index="0" data-posgroup="1" data-freq="17821" lang="fr" title="<div class='nobold'>See examples translated by <em class='translation'>bonjour</em><br>Adverb<br>(+10k examples with alignment)</div>">
          <div class="pos-mark">
              <span class="adv" title="Adverb"></span>
                  </div>
          bonjour</a>"""
soup = BeautifulSoup(anchor, 'html.parser')
print(soup.find_all('a', {'class': 'adv'}))