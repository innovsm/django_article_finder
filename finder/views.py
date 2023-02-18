from django.shortcuts import render
from django.http import HttpResponse
# all functions will be here
from urllib.request import urlopen 
import pandas as pd
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic import TemplateView
import numpy as np
import requests


#-------------------------------------------------------------------------------

def affliation_author(url):
    example = "https://api.crossref.org/v1/works/{}".format(url.split(":")[1].strip().lower())
    print(example)
    try:
        json_data = pd.read_json(example, typ="Series")
        aff_list = []
        aff_list.append(json_data['message']['publisher'])
        try:
            for i in json_data['message']['author']:
                aff_list.append(i['affiliation'][0]['name'])
                print(aff_list)
        except:
            aff_list.append("")
        return aff_list
    except:
        return list(0,0)
def abstract_data(url):
    html = urlopen(url)
    data = BeautifulSoup(html, "html.parser")
    x = data.find("a").find_all_next()[3].attrs['href']
    return x

def journal_issue_volumne(url):
    html = urlopen(url)
    data = BeautifulSoup(html, "html.parser")
    final_list = []
    for i in data.find_all("p"):
        if "Journal" in i.text:
            final_list.append(i.text.split(":")[1])  #journal
        if "Volume" in i.text:
            final_list.append(i.text.split(":")[1])  # volume
        if "Issue" in i.text:
            final_list.append(i.text.split(":")[1])   # issue
    if(len(final_list) < 3):
            
            final_list.append("not found")
            final_list.append("not found")
            final_list.append("not found")
    return final_list

import random
import time
import requests
from bs4 import BeautifulSoup

def scrape_citations(query):
    user_agents = [
        'MyResearchBot/1.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.google.com',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }

    url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query}&btnG="
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    citation_detail = []
    data = soup.find_all("div", class_="gs_ri")
    for item in data:
        title = item.find("h3", class_="gs_rt").text
        author = item.find("div", class_="gs_a").text
        citation = item.find("div", class_="gs_fl").text
        print("Title: ", title)
        print("Author: ", author)
        print("Citation: ", citation)
        x = citation.split(" ")
        y = []
        for alfa in x:
            if(alfa.isnumeric()):
                y.append(alfa)

        citation_detail.append(y[0])

        print("\n")
        
        # Introduce a random sleep time to mimic human behavior
        time.sleep(random.randint(1, 20))
        headers['User-Agent'] = random.choice(user_agents)

    return int(citation_detail[0])


def module(article_name):
    title  = ""
    doi = ""
    download_link = []
    author_names = []
    

    '''-------------------------------------------------------'''
    # modifing the article name to fit the url
    article_name = article_name.lower()  #%2C
    article_name = article_name.replace(",", "%2C")
    article_name = article_name.replace(" ", "+")
    article_name = article_name.replace(":", "%3A")  #' '
    article_name = article_name.replace(' ', "+")
    
    #print(article_name)
    # url of the wikipedia page
    url =  "http://libgen.rs/scimag/"+"?q="+article_name
    html = urlopen(url)
    data = BeautifulSoup(html, "html.parser")
    # extracting the data
    list_raw = []
    for i in  data.find(class_ = "catalog").find_all("td"):
        for j in i.children:
            #print(j)
            list_raw.append(j)
    # printing Doi
    for i in list_raw:
        if("DOI:" in i.text):
            doi += i.text
            break   #caution

    for i in list_raw:
        if((i ==' ') or (i == '\n') or(i == ' ')):
            list_raw.remove(i)
    index = list_raw.index("Mirrors")
    index += 2
    title = list_raw[index]
   # print(title.text)
    title = title.text   # ------------------------------------------ here sis the titile of the article
    '''-------------------------------------------------------'''
  
    index = list_raw.index("Mirrors")
    index+=1
# getting the link
    string_raw = list_raw[index]
    string_raw.rstrip()  # clearning all the white spaces

    new_list = list_raw[-1].children
    for i in new_list:
        for i1 in i.children:
            download_link.append(i1.attrs["href"]) # ----------------- here is the download link
          #  print(i1.attrs["href"])
    list_1 = string_raw.split(";")
    for i in list_1:
        list_temp = i.split(",")
        #print(list_temp)
        counter = len(list_temp)
        author_name = ""
        while(counter >0):
            author_name += list_temp[counter-1]
            author_name += " "
            counter -=1
        author_names.append(author_name)   # -------------------------- here are author name's
    '''-------------------------------------------------------'''
   # print(author_names)
    len_download_link = len(download_link)
    len_author_names = len(author_names)


    return [title, doi, download_link, author_names,len_author_names, len_download_link]




# ---------------------------- app.py function ----------------------------
def article_finder(article_name):
    # modifing the article name to fit the url
    article_name = article_name.lower()
    article_name = article_name.replace(" ", "+")
    article_name = article_name.replace(":", "%3A")
    print(article_name)
    # url of the wikipedia page
    url =  "http://libgen.rs/scimag/"+"?q="+article_name
    html = urlopen(url)
    data = BeautifulSoup(html, "html.parser")

    return data

def evaluator(x):
    if(len(list(x.split(" "))) > 6):
        print(x)
        return x
def final_function(author_name):
    alfa_11 = []
    data = article_finder(author_name)
    test_list = []
    for i in data.find(class_ ="catalog"):
        for i1 in i.find_all_next("p"):
            for alfa in i1.find_all_next("a"):
                test_list.append(alfa.text)

            
    data_1  = pd.DataFrame(test_list)
    data_1.drop_duplicates(inplace =True)
 
    for i in list(data_1[0]):
        data = evaluator(i)
        if(data != None):
            alfa_11.append(data)

    return alfa_11

def date1(url):
    example = "https://api.crossref.org/v1/works/{}".format(url.split(":")[1].strip().lower())
    try:
        json_data = pd.read_json(example, typ="Series")
        return [json_data['message']['title'],json_data['message']['indexed']['date-time']]
    except:
        return ""


#---------------------------------- ALL PROGRAM ENDS HERE-------------------------------------------------------

# Create your views here.
class HomePageView(TemplateView):
    template_name = "alfa.html"

class advanced(TemplateView):

    template_name = "adv.html"
def alfa_request(request):
    if(request.method == 'POST'):
        x_name= request.POST.get('test_name')
        #return HttpResponse("hello case successfully linked {}".format(x_name))
        list_1 = {1:"alfa"}
        return render(request, 'test.html', {"alfa": list_1}) 


#---------------------------------------------------------------

def hello_world(request):

    
    if request.method == 'GET':
        article = request.GET.get('test_name')
    

        try:
           
            article_11 = scrape_citations(article)   # provides the citation info'
            print("1")
            article_22 = module(article)   # provides the article info
            print(article_22[2][1])
            journal_issue_volumne_1 = journal_issue_volumne(article_22[2][1])
            abstract_data_1 = abstract_data(article_22[2][1])
            print("3")
            
            article_aff = affliation_author(article_22[1])
            print("4")
            date_1 = date1(article_22[1])
            print("5")
            
            return render(request,"summary.html",{"article_name":article_22[0],
                "doi":article_22[1],
                "download_link":article_22[2],
                "author_names":article_22[3],
                "abstract_data": abstract_data_1,
                "affliation_data": article_aff[1],
                "publication": article_aff[0],
                "citation": article_11,
                "date": date_1[1],
                "title": date_1[0],
                "journal": journal_issue_volumne_1[0],
                "issue": journal_issue_volumne_1[1],
                "volume": journal_issue_volumne_1[2]  
                })
        
            

            
        except:
            
            return render(request,"partial_info.html",{"article_name":article_22[0],
            "doi":article_22[1],
            "download_link":article_22[2],
            "author_names":article_22[3],
            "abstract_data": abstract_data_1,
            "citation": article_11
            })
  
           
        # title, doi, download_link, author_names,len_author_names, len_download_link
    





#---------------------------------------------------------------------------------


def affliation_author(url):
    example = "https://api.crossref.org/v1/works/{}".format(url.split(":")[1].strip().lower())
    #print(example)
    try:
        json_data = pd.read_json(example, typ="Series")
        aff_list = []
        aff_list.append(json_data['message']['publisher'])
        try:
            university_list = []
            for i in json_data['message']['author']:
    
                university_list.append(i['affiliation'][0]['name'])

            #print(author_list)
            aff_list.append(university_list)
        except:
            
            aff_list.append("")
            aff_list.append(json_data['message']['indexed']['date-time'])  # got date
            aff_list.append(json_data['message']['title'][0])  # got titlle

        author_list = []                                  # got authors details
        for i in json_data['message']['author']:
            alfa = i['given']+" "+i['family']
            author_list.append(alfa)
        aff_list.append(author_list)


            

        #print(aff_list)
        return aff_list
    except:
        return list(0,0,0)
    
#---------------------------------------------------------------------------------

def get_article_adv(article_name): # this function is for finding DOI

    doi_details = []
    final_list_dataframe = []

    for i in range(1,5):
        article_name = article_name.lower()  #%2C
        article_name = article_name.replace(",", "%2C")
        article_name = article_name.replace(" ", "+")
        article_name = article_name.replace(":", "%3A")  #' '
        article_name = article_name.replace(' ', "+")
        try:

            url_link  = "http://libgen.rs/scimag/"+"?q="+article_name+"&page={}".format(i)
            #print(url_link)
            html = urlopen(url_link)
            bs = BeautifulSoup(html, 'html.parser')
            if(bs.text.find("No articles were found") == -1):

                x1_list =bs.find("table").find_all_next("td")
                text_data = []
                for i in x1_list:
                    text_data.append(i.text)
                
                for i in text_data:
                    if i.find("DOI")!= -1:
                        x1 = i.find("DOI")
                        doi_details.append(i[(x1):].rstrip())
                #print(doi_details)
                
            else:
                continue

        except:
            continue
    #------------- PHASE - 2 ---------------------------------------
    
    for i in doi_details:
        try:
            x_1 = affliation_author(i)
            x_2 = ['publication',"affliation",'date','title','author_list']
            
            dict_1 = dict(zip(x_2,x_1))
            final_list_dataframe.append(dict_1)

        except:
            continue
    return pd.DataFrame(final_list_dataframe)


#-------------------------------------------------------


def scrape_scholar(query):
    query = query.lower()
    page_number = 0
    title_details =[]
    author_details = []
    affiliation_details = []
    user_agents = [
        'MyResearchBot/1.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    ]
    headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.google.com',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1'
    }

    while page_number < 40:
        url = f"https://scholar.google.com/scholar?start={page_number}&hl=en&as_sdt=0%2C5&q={query}&btnG="
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find_all("div", class_="gs_ri")
        if not data:
            break
        for item in data:
            title = item.find("h3", class_="gs_rt").text
            author = item.find("div", class_="gs_a").text
            affiliation = item.find("div", class_="gs_rs").text.strip()

            title_details.append(title)
            author_details.append(author)
            affiliation_details.append(affiliation)
            #print(title_details)
           # print(author_details)

        page_number += 10
        # Introduce a random sleep time to mimic human behavior
        time.sleep(random.randint(1, 20))
    return [title_details, author_details, affiliation_details]


#-------------------------------------------------------------
def find_author(x,alfa):
    x = str(x)
    author_name = set(alfa.lower().split())
    target_string = set(x.lower().split())
    if(len(target_string.intersection(author_name)) >= 1):
        return True
    else:
        return False
def find_university(university,university_1):
    university = str(university)
    my_university  = set(university_1.lower().split())
    main_university = set(university.lower().split())
    if(len(main_university.intersection(my_university)) >= 1):
        return True
    else:
        return False


def final_function(name, affiliation,query):
    final_dataset = pd.DataFrame()
    print(name,affiliation)
    # if affiliation is null

    related_data = scrape_scholar(query+" "+name + " "+ affiliation)
    final_dataset["article"] = related_data[0]
    final_dataset['author_details']  = related_data[1]
    final_dataset['affiliation_details'] = related_data[2]
    
    # this case will mactch [KEYWORD , and author name]
    if((affiliation == "") and (name != "")):  # for finding the data using author name

        final_dataset['author_found'] = final_dataset['author_details'].apply(find_author,args=(name,))
        final_dataset['author_found'].replace({None: False},inplace = True)
        related_data_1 = final_dataset[final_dataset['author_found'] == True]
        set_1 = list(related_data_1['article'])

        # if both are present [prefrence to university name , better result]
    elif(((affiliation != "")  and (name == ""))):

        final_dataset['university_found'] = final_dataset['affiliation_details'].apply(find_university,args=(affiliation,))
        final_dataset['university_found'].replace({None: False},inplace=True)
        related_data_1 = final_dataset[final_dataset['university_found'] == True]
        set_1 = list(related_data_1['article'])

    else:
        related_data_1 = final_dataset
        set_1 = related_data[0] # this will be using query, if no [name and affliation ]
    #print(set_1)
    





    



    html_code = []
    for i in set_1:

        html_code.append("<form action = '/adv_details' method = 'get'><input type = 'hidden' name= 'hidden_value' value = '{}'><input type = 'submit' value = 'article_details'></form>".format(i))
    print(len(html_code), related_data_1.shape)
    related_data_1['link'] = html_code
    print(related_data_1)

    return related_data_1



# ==============================================================================

# manager
def manage_adv(request):
    if request.method == 'POST':

        author_name = request.POST.get('author_name')
        affliation_details  = request.POST.get('affliation_name')
        query = request.POST.get('query')
        print(author_name, affliation_details, query)

        
        try:
          
            data_1 = final_function(author_name, affliation_details,query)
            html_table = data_1.to_html(escape=False)
         
            return render(request, 'adv_table.html', {'html_table': html_table})

        except:
            return HttpResponse("error")
# handling advanced request


def hello_world_adv(request):
        if request.method == 'GET':
            article = request.GET.get('hidden_value')
            try:
                article_11 = scrape_citations(article)   # provides the citation info'
                print("1")
                article_22 = module(article)   # provides the article info
                print("2")
                abstract_data_1 = abstract_data(article_22[2][1])
                print("3")
                article_aff = affliation_author(article_22[1])
                print("4")
                date_1 = date1(article_22[1])
                print("5")

            except:
                return HttpResponse("Error had occured")
            return render(request,"summary.html",{"article_name":article_22[0],

            "doi":article_22[1],
            "download_link":article_22[2],
            "author_names":article_22[3],
            "abstract_data": abstract_data_1,
            "affliation_data": article_aff[1],
            "publication": article_aff[0],
            "citation": article_11,
            "date": date_1[1],
            "title": date_1[0]
            })
