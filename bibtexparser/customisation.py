#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License:


__all__ = ['getnames', 'author', 'editor', 'journal', 'keyword', 'link', 
           'page', 'doi', 'type']


def getnames(names):
    """Make people names as surname, firstnames
    or surname, initials. Should eventually combine up the two

    :param names: a list of names
    :type names: list
    :return: list -- Correctly formated names
    """
    tidynames = []
    for namestring in names:
        namestring = namestring.strip()
        if len(namestring) < 1:
            continue
        if ',' in namestring:
            namesplit = namestring.split(',', 1)
            last = namesplit[0].strip()
            firsts = [i.strip().strip('.') for i in namesplit[1].split()]
        else:
            namesplit = namestring.split()
            last = namesplit.pop()
            firsts = [i.replace('.', ' ').strip() for i in namesplit]
        if last in ['jnr', 'jr', 'junior']:
            last = firsts.pop()
        for item in firsts:
            if item in ['ben', 'van', 'der', 'de', 'la', 'le']:
                last = firsts.pop() + ' ' + last
        tidynames.append(last + ", " + ' '.join(firsts))
    return tidynames


def author(record):
    """

    """
    if "author" in record:
        if record["author"]:
            record["author"] = getnames([i.strip() for i in record["author"].replace('\n', ' ').split(" and ")])
        else:
            del record["author"]
    return record


def editor(record):
    """

    """
    if "editor" in record:
        if record["editor"]:
            record["editor"] = getnames([i.strip() for i in record["editor"].replace('\n', ' ').split(" and ")])
            # convert editor to object
            record["editor"] = [{"name": i, "id": i.replace(',', '').replace(' ', '').replace('.', '')} for i in record["editor"]]
        else:
            del record["editor"]
    return record


def page(record):
    """

    """
    if "pages" in record:
        if "-" in record["pages"]:
            p = [i.strip().strip('-') for i in record["pages"].split("-")]
            record["pages"] = p[0] + ' to ' + p[-1]
    return record


def type(record):
    """

    """
    if "type" in record:
        record["type"] = record["type"].lower()
    return record


def journal(record):
    """

    """
    if "journal" in record:
        # switch journal to object
        if record["journal"]:
            record["journal"] = {"name": record["journal"], "id": record["journal"].replace(',', '').replace(' ', '').replace('.', '')}

    return record


def keyword(record):
    """

    """
    if "keyword" in record:
        record["keyword"] = [i.strip() for i in record["keyword"].replace('\n', '').split(",")]

    return record


def link(record):
    """

    """
    if "link" in record:
        links = [i.strip().replace("  ", " ") for i in record["link"].split('\n')]
        record['link'] = []
        for link in links:
            parts = link.split(" ")
            linkobj = {"url": parts[0]}
            if len(parts) > 1:
                linkobj["anchor"] = parts[1]
            if len(parts) > 2:
                linkobj["format"] = parts[2]
            if len(linkobj["url"]) > 0:
                record["link"].append(linkobj)

    return record


def doi(record):
    """

    """
    if 'doi' in record:
        if 'link' not in record:
            record['link'] = []
        nodoi = True
        for item in record['link']:
            if 'doi' in item:
                nodoi = False
        if nodoi:
            link = record['doi']
            if link.startswith('10'):
                link = 'http://dx.doi.org/' + link
            record['link'].append({"url": link, "anchor": "doi"})
    return record
