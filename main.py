import requests
import pandas as pd   #to populate excel
from bs4 import BeautifulSoup  # beautifulsoup parses HTML page and create tree structure to data fetch
import random
from yaml import parse

# global array to accomodate all reviews
reviewlist = []

# using proxy
def getRandomProxy():
    proxy = {
        "http":f"http://kh072ICB0vRFURg9:wifi;;@proxy.soax.com:{9000 + random.randint(0,9)}",
        "https":f"http://kh072ICB0vRFURg9:wifi;;@proxy.soax.com:{9000 + random.randint(0,9)}"
    }
    return proxy

def extractReview(reviewUrl,pageNumber):
    resp = requests.get(reviewUrl,proxies=getRandomProxy())
    soup = BeautifulSoup(resp.text,'html.parser')
    reviews = soup.findAll('div',{'data-hook':"review"})
    # print(reviews)
    for item in reviews:
        with open('outputs/file.html',"w",encoding="utf-8") as f:
            f.write(str(item))
        review = {
            'productTitle':soup.title.text.replace("Amazon.in Customer reviews: ", "").strip(),
            'Review Title':item.find('a',{'data-hook':'review-title'}).text.strip(),
            'Rating':item.find('i',{'data-hook':'review-star-rating'}).text.strip(),
            'Review Body':item.find('span',{'data-hook':'review-body'}).text.strip()
        }
        reviewlist.append(review)
        break

def totalPages(reviewUrl):
    resp = requests.get(reviewUrl,proxies=getRandomProxy())
    soup = BeautifulSoup(resp.text,'html.parser')
    reviews = soup.find('div',{'data-hook':"cr-filter-info-review-rating-count"})
    return int(reviews.text.strip().split(', ')[1].split(' ')[0].replace(',', ''))  # to get integer number of reviews from total
    
def main():
    productUrl = "https://www.amazon.in/OnePlus-Nord-Black-128GB-Storage/dp/B09WQY65HN/ref=sr_1_1?crid=EMUVZHC3TAVE&keywords=oneplus%2B7&qid=1657352917&sprefix=one%2Bplus%2Caps%2C423&sr=8-1&th=1" 
    reviewUrl = productUrl.replace("dp","product-reviews") + "?pageNumber=" + str(1) 
    totPages = totalPages(reviewUrl)
    
    for i in range(totPages//10):  #since each page can accomodate 10 reviews
        print(f'Running for page {i}')
        try:
            reviewUrl = productUrl.replace("dp","product-reviews") + "?pageNumber=" + str(i) 
            extractReview(reviewUrl,i)
        except Exception as e:
            print(e)    
    
    # creating a dataframe from reviewlist
    df = pd.DataFrame(reviewlist)
    df.to_excel('output.xlsx',index=False)
    
main()    