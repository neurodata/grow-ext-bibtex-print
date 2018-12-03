import re
from datetime import datetime

import bibtexparser
from bibtexparser.bparser import BibTexParser
from jinja2 import nodes
from jinja2.ext import Extension
import pandas as pd

def load_bibtex_by_month(bibfile):
    
    MONTH_CONVERT = {'jan': 1, 'Jan': 1, 'January': 1, 'feb': 2, 'Feb': 2, 'February': 2, 'mar': 3, 'Mar': 3, 'March': 3, 'apr': 4, 'Apr': 4, 'April': 4, 'may': 5, 'May': 5, 'june': 6, 'June': 6, 'jul': 7, 'july': 7, 'July': 7, 
       'aug': 8, 'Aug': 8, 'August': 8, 'sep': 9, 'Sep': 9, 'september': 9, 'September': 9, 'oct': 10, 'Oct': 10, 'october': 10, 'October': 10, 'nov': 11, 'Nov': 11, 'November': 11}
    
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False

    with open(bibfile) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    bib_entries = pd.DataFrame(bib_database.entries)
    bib_entries['mo_num'] = bib_entries.loc[:, 'month'].map(mon, na_action='ignore').fillna(0).astype(int)  # Make a new column in DataFrame containing the month number
    bib_entries.sort_values(by=['year', 'mo_num'], ascending=False, inplace=True)
    
    
    return bib_entries.to_dict(orient='records')

def load_bibtex(bibfile):
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False

    with open(bibfile) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    bib_entries = bib_database.entries
    bib_entries.sort(key=lambda x: x.get('author', ''))
    bib_entries.sort(key=lambda x: x.get('year', ''), reverse=True)

    return bib_entries


def print_authors(bib_entry):
    authors = bib_entry['author'].split(' and ')

    auths_format = []
    for author in authors:
        names = author.split(', ')
        last = names[0]
        if last[0] == '{' and last[-1] == '}':
            last = last[1:-1]
        initials = []
        if len(names) > 1:
            for n in names[1].split(' '):
                if len(n) > 1:
                    initials += n[0] + '. '
                else:
                    initials += n + '. '
        full_name_format = ''.join(initials) + last
        auths_format.append(full_name_format)

    # return et al if # of auths_format > 3
    if len(auths_format) > 3:
        return auths_format[0] + ' et al.'
    elif len(auths_format) == 1:
        return auths_format[0] + '.'
    else:
        return u'{} and {}.'.format(', '.join(auths_format[0:-1]), auths_format[-1])


def print_link(bib_entry):
    if 'doi' in bib_entry:
        return 'https://doi.org/' + bib_entry['doi']
    if 'url' in bib_entry:
        return bib_entry['url']
    if 'arxivid' in bib_entry:
        arxivID = bib_entry['arxivid'].replace('arXiv:', '')
        return 'https://arxiv.org/abs/{}'.format(arxivID)
    print('{} did not have a link'.format(bib_entry['ID']))
    # print('here are the keys')
    # for key in bib_entry:
    #     print(key)


def print_venue(bib_entry):
    if 'journal' in bib_entry:
        return bib_entry['journal']

    # probably a conference
    if 'booktitle' in bib_entry:
        return bib_entry['booktitle']


def print_title(bib_entry):
    title = bib_entry['title']

    if title[0] == '{' and title[-1] == '}':
        title = title[1:-1]

    if '\href' in title:
        m = re.findall(r"\\href\{(.+)\}{(.+)}", title)
        link = m[0][0]
        t = m[0][1]
        title = "<a href={}>{}</a>".format(link, t)

    return title


def print_issue_data(bib_entry):
    if 'pages' in bib_entry and 'number' in bib_entry and 'volume' in bib_entry:
        return print_issue(bib_entry) + print_volume(bib_entry) + print_pages(bib_entry)
    else:
        return ''


def print_pages(bib_entry):
    pages = bib_entry['pages']
    pages = pages.replace('--', '-')
    return ':' + pages + ', '


def print_volume(bib_entry):
    return '{}'.format(bib_entry['volume'])


def print_issue(bib_entry):
    return '({})'.format(bib_entry['number'])


def print_current_year(_):
    return datetime.now().year


class BIBTEX_PRINT(Extension):

    def __init__(self, environment):
        super(BIBTEX_PRINT, self).__init__(environment)
        environment.filters['load_bibtex'] = load_bibtex
        environment.filters['print_authors'] = print_authors
        environment.filters['print_link'] = print_link
        environment.filters['print_title'] = print_title
        environment.filters['print_venue'] = print_venue
        environment.filters['print_issue_data'] = print_issue_data
        environment.filters['print_current_year'] = print_current_year
