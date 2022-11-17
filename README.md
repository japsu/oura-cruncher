# Oura sleep cruncher

Sleep better with the power of data.

## Getting started

Place an Oura API Personal Access Token in a file called `.token`.

    python -m venv venv
    source venv/bin/activate
    pip install -U pip setuptools wheel
    pip install -r requirements.txt
    python -m oura_cruncher

## Features

### Oura API v2 integration

* [X] Load night sleep from Oura API v2
* [ ] Yeet `oura`, use `requests` instead

### Google Sheets integration

Use Google Sheets as a makeshift UI to add labels and visualize data.

* [ ] Update a Google Sheet with data extracted from Oura API
* [ ] Read labels from a Google Sheet

### Statistical tests

Perform statistical tests on hypotheses such as "I sleep better on nights with label X than without".

* [ ] Single label test
* [ ] Correlation between bedtime and efficiency
