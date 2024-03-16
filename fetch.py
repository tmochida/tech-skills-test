#!/usr/local/bin/python3
# Script for fetching web page content / metadata

import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from pathlib import Path
import re
import requests
from typing import List
import validators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_web_protocol(url: str) -> bool:
    """Check if URL uses HTTP or HTTPS protocol"""
    return bool(re.match("http[s]?://.+", url.lower()))


def local_path(url: str) -> Path:
    """Return local file path for a URL. The filename is defined as:
    1. URL with protocol identifier removed
    2. If URL does not end with .html, it will be added"""
    if '://' in url:
        url = url.split('://')[1]
    url = url if url.endswith('.html') else url + '.html'

    return Path.cwd().joinpath(url)


def save_url_content(url: str, r: requests.Response):
    """Save content of requests.Response to a local file"""
    path = local_path(url)
    with open(path, 'w') as fd:
        fd.write(r.text)


def fetch_urls(urls: List[str], raise_exception: bool = False):
    """Make a GET request for each url and save results locally"""
    for u in urls:
        u = u.strip()

        # url validation        
        if not is_web_protocol(u):
            if '://' in u:
                logger.error(f'URL needs to use HTTP or HTTPS protocol: {u}')
                if raise_exception:
                    raise ValueError(f'non-web protocol used for URL {u}')
                continue
            u = f'https://{u}'
        if not validators.url(u):
            logger.error(f'Invalid URL supplied: {u}')
            if raise_exception:
                raise ValueError(f'invalid URL {u}')
            continue

        # fetch content
        logger.info(f'Fetching content for {u}')
        try:
            resp = requests.get(u)
            if resp.status_code != requests.codes.ok:
                logger.error(f"received HTTP status {resp.status_code}")
                resp.raise_for_status()
            save_url_content(u, resp)
        except Exception as e:
            logger.error(f'Error during fetch: {e}')
            if raise_exception:
                raise e
            continue


def load_page_metadata(urls: str):
    """Load metadata for url and print to stdout"""
    for url in urls:
        logger.info(f'Loading metadata for {url}')
        # fetch url if not yet fetched
        path = local_path(url)
        if not path.exists():
            logger.info(f'{url} not yet fetched, fetching now')
            try:
                fetch_urls([url], raise_exception=True)
            except:
                logger.error(f'Failed to fetch URL {url}, unable to show metadata')
                continue

        mtime = datetime.fromtimestamp(path.stat().st_mtime)

        # load HTML DOM and search for links and images
        with open(path) as fd:
            # assumes all pages are HTML to suppress warnings from library.
            # NOTE: needs adjustments to support non-HTML (e.g. XHTML) links
            soup = BeautifulSoup(fd, 'html.parser')

        links = soup.find_all('a')
        images = soup.find_all('img')

        print(f'site: {path.stem}')
        print(f'num_links: {len(links)}')
        print(f'images: {len(images)}')
        print(f'last_fetch: {mtime}\n')


def main():
    parser = argparse.ArgumentParser(
        prog='Web Fetcher',
        description='Fetches web pages and assets',
    )
    parser.add_argument("urls", action="extend", nargs="+", type=str,
                        help="list of URLs to fetch")
    parser.add_argument("--metadata", action="store_true",
                        help="show metadata of URLs. URLs that have not been fetched will be fetched")
    args = parser.parse_args()

    if args.metadata:
        load_page_metadata(args.urls)
    else:
        fetch_urls(args.urls)


if __name__ == "__main__":
    main()