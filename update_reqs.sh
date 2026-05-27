#!/bin/bash

source venv/bin/activate

# Source - https://stackoverflow.com/a/68978982
# Posted by haulpd, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-26, License - CC BY-SA 4.0

pip3 freeze | cut -d"=" -f1 > requirements.txt

# pip-chill --no-version
