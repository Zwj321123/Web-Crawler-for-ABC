import requests
from bs4 import BeautifulSoup
import urllib
import os.path

url = "https://abcnews.go.com/"
save_path = 'E:\study\其他\实习\web crawler' #add your own path here
#request header
response = requests.get(url)
#analyze websource code, and acquire titles
root = BeautifulSoup(response.text, 'html.parser')
titles = root.find_all("div", class_="headlines-li-div")
#print(titles)
index = 0
for title in titles:
    if title.h1.a != None:
        print(title.h1.a.string)
        url = title.h1.a['href']
        #print(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            #crawl date:
            content = soup.find('meta', { 'property': 'lastPublishedDate' })
            print(content['content'])
            
            #crawl content:
            list = [p.text for p in soup.body.find_all("p")]
          
            path = save_path + '\Article' #save content into Article file as .txt format
            completeName = os.path.join(path, str(index)+".txt")
            file1 = open(completeName, "w")
            with file1 as output:
                output.write(str(list))
            file1.close()
            #crawl image:
            try:
                ImUrl = soup.find('meta', {'property':'og:image'})['content']
                #print(ImUrl)
                path2 = save_path + '\image'    #save content into Article file as .jpg format
                completeName2 = os.path.join(path2, str(index)+".jpg")
                f = open(completeName2, 'wb')
                request = urllib.request.urlopen(ImUrl)
                buf = request.read()
                f.write(buf)
                f.close()
            except:
                pass
            index = index + 1
        except:
            pass
print('finish')
