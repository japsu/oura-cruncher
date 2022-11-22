# Oura sleep cruncher

Sleep better with the power of data.

## Getting started

Get a `credentials.json` from Google API management UI.

    # create config and edit it to your liking
    cp config.sample.toml config.toml
    code config.toml

    # create venv and install deps
    python -m venv venv
    source venv/bin/activate
    pip install -U pip setuptools wheel
    pip install -r requirements.txt

    # run!
    python -m oura_cruncher

On first run, it will ask you to authenticate to Google APIs.

If successful, this will download all nights from Oura and place them in the Google Sheet.
## Features

### Oura API v2 integration

* [X] Load night sleep from Oura API v2
* [ ] Yeet `oura`, use `requests` instead

### Google Sheets integration

Use Google Sheets as a makeshift UI to add labels and visualize data.

* [X] Update a Google Sheet with data extracted from Oura API
* [ ] Read labels from a Google Sheet

### Statistical tests

Perform statistical tests on hypotheses such as "I sleep better on nights with label X than without".

* [ ] Single label test
* [ ] Correlation between bedtime and efficiency
