# -*- encoding: UTF-8 -*-

from bs4 import BeautifulSoup
from os import path
from pelican import signals, readers, contents

import collections
import re


def toc(content):
    if isinstance(content, contents.Static):
        return
    soup = BeautifulSoup(content._content, 'html.parser')
    filename = content.source_path
    extension = path.splitext(filename)[1][1:]
    toc = None
    # Markdown File
    if extension in readers.MarkdownReader.file_extensions:
        toc = soup.find_all('h2', {"id": re.compile('^\w+$')})
        toc_list = collections.OrderedDict()
        for entry in toc:
            toc_list[(entry['id'])] = unicode(entry.getText())
        content.toc = toc_list


def register():
    signals.content_object_init.connect(toc)
