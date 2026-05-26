source venv/bin/activate

# Source - https://stackoverflow.com/a/3452888
# Posted by rbp, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-26, License - CC BY-SA 4.0

pip --disable-pip-version-check list --outdated --format=json | python -c "import json, sys; print('\n'.join([x['name'] for x in json.load(sys.stdin)]))" | xargs -n1 pip install -U
