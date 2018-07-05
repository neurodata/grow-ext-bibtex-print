import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from jinja2.ext import Extension


def load_bibtex(bibfile):
    parser = BibTexParser()
    parser.ignore_nonstandard_types = False

    with open(bibfile) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    bib_entries = bib_database.entries
    bib_entries.sort(key=lambda x: x['author'])
    bib_entries.sort(key=lambda x: x['year'], reverse=True)

    return bib_entries


def print_authors(bib_entry):
    authors = bib_entry['author'].split(' and ')

    auths_format = []
    for author in authors:
        names = author.split(', ')
        last = names[0]
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
        return auths_format[0]
    else:
        return ', '.join(auths_format[0:-1]) + ' and ' + auths_format[-1]


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


class BIBTEX_PRINT(Extension):

    def __init__(self, environment):
        super(BIBTEX_PRINT, self).__init__(environment)
        environment.filters['load_bibtex'] = load_bibtex
        environment.filters['print_authors'] = print_authors
        environment.filters['print_link'] = print_link
        environment.filters['print_title'] = print_title
        environment.filters['print_venue'] = print_venue
        environment.filters['print_issue_data'] = print_issue_data
