import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Comment
import requests
import time

scraped = set()  # set of urls we've extracted from or are blacklisted
seen = set()
unique_urls = set()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if (resp.status >= 400 or resp.status == 204) or (url in scraped):
        return list()

    #Implementation requred.
    #print("in extract_next_links")
    soup = BeautifulSoup(resp.raw_response.content, "lxml")
    
    for tag in soup(text=lambda text: isinstance(text,Comment)):
        tag.extract()

    for element in soup.findAll(['script', 'style']):
        element.extract() 

    #this is what to send to the tokenizer
    webtext = soup.get_text()

    #print(url)
    #print(soup.get_text())
   # tokenize(soup.get_text())
    links = set()
    
    for link in soup.find_all('a'):
    # get absolute urls here before adding to listLInks()
        childURL = link.get('href')

        if is_valid(childURL) and childURL not in seen:
            #print(childURL)
            links.add(childURL) 
            seen.add(childURL) 

    #for link in links:
        #print (link)
        
    scraped.add(url)
    return list(links)


def is_valid(url):
    #valid_domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu", "today.uci.edu/department/information_computer_sciences"]
    try:
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https", "today"]):
            return False
       # if not any(x in parsed.netloc for x in valid_domains):
        #    return False
        #if parsed.netloc not in set(["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu", "today.uci.edu/department/information_computer_sciences"]):
         #   return False
        if not re.match(
            r'^(\w*.*)(ics.uci.edu|cs.uci.edu|stat.uci.edu|today.uci.edu\/department\/information_computer_sciences)$',parsed.netloc):
            return False
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False
        # This is a good URL, we can use it
        unique_urls.add(parsed.netloc)
        return True


    except TypeError:
        print ("TypeError for ", parsed)
        raise

def printList():
    f = open("URLS.txt", "a")

    for word in scraped:
        f.write(word + "\n")

    f.write("\n\n\n\nUNIQUE URLS")

    for word in unique_urls:
        f.write(word + "\n")

    f.close()