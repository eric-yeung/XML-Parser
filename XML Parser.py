import csv
import requests
import xml.etree.ElementTree as ET

def RSSLoader():
    
    url = 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml'

    resp = requests.get(url)

    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)

def parseXML(xmlfile):

    tree = ET.parse(xmlfile)

    root = tree.getroot()

    newsItems = []

    for item in root.findall('./channel/item'):

        news = {}
        
        for child in item:

            if child.tag == '{http://search.yahoo.com/mrss/}content':
                news['media'] = child.attrib['url']

            elif child.text is not None:
                news[child.tag] = child.text.encode('utf8')
        
        newsItems.append(news)
    
    print(news.keys())

    del news['{http://purl.org/dc/elements/1.1/}creator']
    
    
    print(news.keys())

    return newsItems

def saveToCSV (newsItems,fileName):

    fields = ['guid', 'title', 'description', 'link', 'media','pubDate','category', '{http://search.yahoo.com/mrss/}description', '{http://search.yahoo.com/mrss/}credit', '{http://purl.org/dc/elements/1.1/}creator']
    # fields = ['guid', 'title', 'description', 'link', 'media','pubDate','category']
    with open(fileName, 'w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames = fields)

        writer.writeheader()

        writer.writerows(newsItems)

def main():

    RSSLoader()

    newsItems = parseXML('topnewsfeed.xml')

    saveToCSV(newsItems, 'topnews.csv')

if __name__ == "__main__":
    main()