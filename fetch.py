#!/usr/bin/python3
# Script for fetching web page content / metadata

import argparse
from bs4 import BeautifulSoup
import re
import requests
from typing import List
import validators


def is_web_protocol(url: str) -> bool:
    """Check if URL uses HTTP or HTTPS protocol"""
    return bool(re.match("http[s]?://.+", url.lower()))


def local_filename(url: str) -> str:
    """Return local filename for a URL. The filename is defined as:
    1. URL with protocol identifier removed
    2. If URL does not end with .html, it will be added"""
    if "://" in url:
        url = url.split("://")[1]
    return url if url.endswith(".html") else url + ".html"


def save_url_content(url: str, r: requests.Response):
    """Save content of requests.Response to a local file"""
    with open(local_filename(url), "w") as fd:
        fd.write(r.text)


def fetch_urls(urls: List[str]):
    for u in urls:
        u = u.strip()

        # url validation        
        if not is_web_protocol(u):
            u = f'https://{u}'
        if not validators.url(u):
            print(f'Invalid URL supplied: {u}')
            continue

        # fetch content
        print(f"Fetching content for {u}")
        try:
            resp = requests.get(u)
            if resp.status_code != requests.codes.ok:
                print(f"received HTTP status {resp.status_code}")
                resp.raise_for_status()
            save_url_content(u, resp)
        except Exception as e:
            print(f"Error during fetch: {e}")
            continue


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
        pass  # TODO implement metadata parsing
    
    fetch_urls(args.urls)


if __name__ == "__main__":
    main()