import requests
from bs4 import *
homepage = requests.get("https://www.amazon.in/gp/bestsellers/books/")
soup = BeautifulSoup(homepage.content, 'lxml')
fw = open("in_book.csv", "w")
fw.write("Name;URL;Author;Price;Number of Ratings;Average Rating\n")

pages = soup.find("div", {"id": 'zg_paginationWrapper'})

for link in pages.find_all('a'):

    pg = link.get('href')
    page = requests.get(pg)
    soup = BeautifulSoup(page.content, 'lxml')

    dataset = soup.findAll("div", {"class": "zg_itemImmersion"})
    i = 0
    name, author, price, nor, rating, link = "", "", "", "", "", ""
    for data in dataset:
        i += 1
        nametag = data.find(
            "div", {"class": "p13n-sc-truncate p13n-sc-line-clamp-1"})
        if nametag is None:
            name = 'Not available'
        else:
            name = nametag.get_text().strip()

        linktag = nametag.find_previous("a")
        if linktag is None:
            link = 'Not available'
        else:
            link = "https://www.amazon.in"+linktag.get('href')

        authortag = nametag.find_next("div")
        if authortag is None:
            author = 'Not available'
        else:
            author = authortag.get_text().strip()

        pricetag = data.find("span", {"class": "p13n-sc-price"})
        if pricetag is None:
            price = 'Not available'
        else:
            price = pricetag.get_text().strip()

        nortag = data.find("a", {"class": "a-size-small a-link-normal"})
        if nortag is None:
            nor = 'Not available'
        else:
            nor = nortag.get_text().strip()

        ratingtag = data.find("span", {"class": "a-icon-alt"})
        if ratingtag is None or ratingtag.get_text().strip() == 'Prime':
            rating = 'Not available'
        else:
            rating = ratingtag.get_text().strip()

        fw.write(name+";"+link+";"+author+";"+price+";"+nor+";"+rating+"\n")
