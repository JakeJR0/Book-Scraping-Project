import requests, re
import pandas as pd
from bs4 import BeautifulSoup
import FileControl

colours = None
site_count = 0
file = FileControl.FileController()

def get_soup(url):
    global site_count
    """ Returns a soup object """

    r = requests.get(url)
    site_count += 1
    return BeautifulSoup(r.text, 'html.parser')

def get_book_lists(soup, site=""):
  """ Returns a list of book lists """
  
  sites = soup.find_all('a', {'class': 'listTitle'})
  urls = []
  
  for i in sites:
    urls.append("{}{}".format(site, i['href']))

  return urls

def get_book_list_data(book_site, book_list_site, frame=pd.DataFrame):
  global site_count
  book_list_soup = get_soup(book_list_site)

  for book_list in book_list_soup:
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
        site_update = "Site {}: Registered".format(site_count)
        
        try:
          colours.print_message(site_update)
        except AttributeError:
          print("{} (GoodReads file has not been setup)".format(site_update))


def get_books(soup):
    """ Returns a list of books """
    return soup.find_all('tr', {'itemtype': 'http://schema.org/Book'})


def get_title(book):
    """ Returns the title of the book """
    return book.find('span', {'itemprop': 'name'}).text


def get_thumbnail(book):
    """ Returns the thumbnail of the book """
    return book.find('img', {'class': 'bookCover'})['src']


def get_description(book, site):
    """ Returns the description of the book """

    link = get_link(book, site)
    soup = get_soup(link)
    span = soup.find('div', {'class': 'BookPageMetadataSection__description'})
    soup = BeautifulSoup(str(span), 'html.parser')
    desc = soup.get_text()
    desc = desc.replace(".", ". ")
    desc = desc.replace("  ", " ")
  
    return desc


def get_link(book, site):
    """ Returns the link to the book """
    return site[:-1] + book.find('a', {'class': 'bookTitle'})['href']


def GoodReads(filename="Test.sql"):
    global site_count
    site = "https://www.goodreads.com/"
    soup = get_soup(site)
    regx = re.compile("/genres/+")
    book_sites_links = soup.find_all("a", {'class': 'gr-hyperlink'}, href=regx)
    site_count = 0

  
    for s in book_sites_links:
      book_list_site = site[:-1] + s['href']
      get_book_list_data(site, book_list_site)

def setup(**kwargs):
  global colours
  
  terminal_colors = kwargs["terminal_colors"]
  colours = terminal_colors
  
  if colours is not None:
    FileControl.setup(terminal_colors=colours)

if __name__ == "__main__":
    GoodReads()
