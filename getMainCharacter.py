import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import webbrowser

def main():
    mainCharacter = input("Which character would you like to find? ")
    url = input("What is the url of the search results you would like to filter? ")
    max_pages = eval(input("How many pages would you like to search? (Cannot be more than 50) "))

    if max_pages > 50:
        max_pages = 50

    pagesSearched = 0
    while pagesSearched < max_pages:
        soup = makeSoup(url)
        works = getWorks(soup)
        
        getMyGirl(works, mainCharacter)

        pagesSearched += 1
        print("finished searching page " + str(pagesSearched))

        next = soup.find("a", {"rel": "next"})
        
        if next is None:
            break

        url = "https://archiveofourown.org" + next["href"]

def makeSoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def getWorks(soup):
    return soup.find_all("li", "work blurb group")

def getMyGirl(works, mainCharacter):
    for work in works:
        characters = work.find_all("li", "characters")
        
        for character in characters[:1]:
            name = character.find("a").text.lower()
            
            if mainCharacter.lower() in name:
                url = "https://archiveofourown.org" + work.find("a")["href"]
                openFicsOfMyGirl(url)

def openFicsOfMyGirl(url):
    try:
        browser = webbrowser.get("firefox")
        browser.open_new_tab(url)
    except:
        print("couldn't open " + url)

main()
