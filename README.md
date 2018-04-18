# grow-ext-bibtex-print

BibTeX extension for Grow.

## Concept

Installs a filter into the Jinja2 environment to print references from bibtex file.

## Usage

### Initial setup

1. Create an `extensions.txt` file within your pod.
1. Add to the file: `git+git://github.com/falkben/grow-ext-bibtex-print`
1. Ensure `.gitignore` contains `extensions`.
1. Run `grow install`.
1. Add the following section to `podspec.yaml`:

```
extensions:
  jinja2:
  - extensions.bibtex_print.bibtex_print.BIBTEX_PRINT
```

### In templates

```
# load the bibtex file into your template
{% set PUBS = 'content/pubs/pubs.bib'|load_bibtex %}

# Print some references:
{% for item in PUBS %}
    {{item|print_authors}}
    <a href="{{item|print_link}}" target="_blank">{{item|print_title|render|safe}}</a>.
    In <i>{{item|print_venue}}</i>, {{item|print_issue_data}}{{item.year}}.
{% endfor %}

# Outputs the following HTML.



```