"""
  Project Name: Book Scraping Project
  File Name: good_reads.py

  Description:
    This file is in-change of web-scraping the
    goodreads website.
"""

import re
import requests
from bs4 import BeautifulSoup

import file_control

Terminal = file_control.visual_elements.Terminal

file = file_control.FileController()


def get_soup(url):
    """ Returns a soup object """

    while True:
        try:
            req = requests.get(url, timeout=10)
            break
        except requests.exceptions.ConnectTimeout:
            Terminal.print_error("Connection Timed Out")
            Terminal.print_warning("Retrying...")
        except requests.exceptions.ReadTimeout:
            Terminal.print_error("Connection Timed Out")
            Terminal.print_warning("Retrying...")

    return BeautifulSoup(req.text, "html.parser")


def get_book_lists(soup, site=""):
    """Returns a list of book lists"""

    sites = soup.find_all("a", {"class": "listTitle"})
    urls = []

    for i in sites:
        site_url = i["href"]
        urls.append(f"{site}{site_url}")

    return urls


def get_book_list_data(book_site, book_list_site):
    """
    This gets a list of books from the site provided.
    """

    book_list_soup = get_soup(book_list_site)

    for _ in book_list_soup:
        urls = get_book_lists(book_list_soup, book_site[:-1])
        for url in urls:
            list_book_soup = get_soup(url)
            books = get_books(list_book_soup)
            for book in books:
                title = get_title(book)
                desc = get_description(book, book_site)
                thumb = get_thumbnail(book)
                link = get_link(book, book_site)

                file.add(title, desc, thumb, link)
                site_update = f"Site {link}: Registered"

                # Ensures that the program does not error
                # if the file did not get setup.
                try:
                    Terminal.print_message(site_update)
                except AttributeError:
                    print(f"{site_update} (GoodReads file has not been setup)")


def get_books(soup):
    """Returns a list of books"""
    return soup.find_all("tr", {"itemtype": "http://schema.org/Book"})


def get_title(book):
    """
    Returns the title of the book
    """
    return book.find("span", {"itemprop": "name"}).text


def get_thumbnail(book):
    """Returns the thumbnail of the book"""
    return book.find("img", {"class": "bookCover"})["src"]


def get_description(book, site):
    """Returns the description of the book"""

    link = get_link(book, site)
    soup = get_soup(link)
    span = soup.find("div", {"class": "BookPageMetadataSection__description"})
    soup = BeautifulSoup(str(span), "html.parser")
    desc = soup.get_text()
    desc = desc.replace(".", ". ")
    desc = desc.replace("  ", " ")

    return desc


def get_link(book, site):
    """Returns the link to the book"""
    return site[:-1] + book.find("a", {"class": "bookTitle"})["href"]


def good_reads():
    """
    This is the main function, by running this
    it starts web-scrapping from the site variable as
    a base url.

    This function works through all the available links
    that link to books.
    """

    site = "https://www.goodreads.com/"

    soup = get_soup(site)

    # Ensures the web scrapper stays in the
    # genres path of the site.

    regx = re.compile("/genres/+")

    book_sites_links = soup.find_all("a", {"class": "gr-hyperlink"}, href=regx)

    for site_link in book_sites_links:
        book_list_site = site[:-1] + site_link["href"]
        get_book_list_data(site, book_list_site)


if __name__ == "__main__":
    good_reads()
