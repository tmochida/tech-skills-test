# tech-skills-test
Temporarily holds code for technical tests / take home assignments

## Web page fetch CLI
`fetch.py` implements the web page fetch CLI for the take home test.

## Followups / TODO
1. Add unit tests
2. Fetch assets (e.g. links to JS/CSS/img) and save them under `<site>_assets` directory to support offline viewing
3. Add a staleness config to re-fetch web pages fetched more than N minutes ago (e.g. refresh pages fetched more than 1 hour ago)

## Install
1. Run `docker build -t fetchcli .`
2. Start the container with `docker run -i -t fetchcli /bin/bash`. A bash shell will open in `/opt/fetch` directory.
3. Run the fetch CLI: `./fetch https://www.google.com`