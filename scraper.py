from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup
import ast

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.1 Safari/537.36'}


def searchHLJ(session, model, grade):
    URL = "https://www.hlj.com/search/?Word="+model+"&Page=1&StockLevel=In%C2%A0Stock&StockLevel=Backordered&MacroType2="
    match grade:
        case "HG":
            URL = URL + "High+Grade+Kits"
        case "RG":
            URL = URL + "Real+Grade+Kits"
        case "MG":
            URL = URL + "Master+Grade+Kits"
        case "PG":
            URL = URL + "Perfect+Grade+Kits"
        
    page = session.get(URL, headers=headers)

    page.html.render()

    models = []

    results = page.html.find(".search-widget-block")

    i=0
    while(i<len(results) and i<10):
        model = results[i]
        name = model.find(".product-item-name")[0].text.strip()
        link = "https://www.hlj.com" + model.find(".product-item-name")[0].find("a")[0].attrs['href']
        price = model.find("[class$=stock-left]")[0].text.strip()
        models.append({"name":name,"price":price, "link": link})
        i+=1
    return models

def searchGundamPlanet(session, model, grade):
    URL = "https://www.gundamplanet.com/catalogsearch/result/index/show_in/293/mst_stock/2/?cat="
    match grade:
        case "HG":
            URL = URL + "12"
        case "RG":
            URL = URL + "11"
        case "MG":
            URL = URL + "10"
        case "PG":
            URL = URL + "9"
            
    URL = URL + "&mst_stock=2&product_list_order=relevance&q=" + model + "&isAjax=true"
    
    page = session.get(URL, headers=headers)
    
    page.html.render()
    
    try:
        
        print(ast.literal_eval(page.html.text)["products"])
        html = "<html>" + ast.literal_eval(page.html.text)["products"] + "</html>"
        
        html = html.replace("\\", "")
        
        
        soup = BeautifulSoup(html, 'html.parser')
        
        models = []
        
        results = soup.select('.product-item-info')
    

    
        i=0
        while(i<len(results) and i<10):
            model = results[i]
            name = model.select(".product-item-link")[0].text.strip()
            link = model.select(".product-item-link")[0].attrs['href']
            price = model.select(".price")[0].text.strip()
            models.append({"name":name,"price":price, "link": link})
            i+=1
        return models
    except Exception as e:
        print(e)


model = input('Enter name of model: ')
model = '+'.join(model.split())

grade = input('Enter grade of model [RG,HG,MG,PG]: ').upper()
while(grade!='RG' and grade!='HG' and grade!='MG' and grade!='PG'):
    grade = input('Invalid grade. Please enter grade from following options [RG,HG,MG,PG]').upper()


session = HTMLSession()

results = searchHLJ(session, model, grade)
results2 = searchGundamPlanet(session, model, grade)

print(results)
print(results2)

input('Press ENTER to exit')
