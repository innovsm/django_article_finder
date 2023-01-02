from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# all functions will be here
from urllib.request import urlopen 
import pandas as pd
from bs4 import BeautifulSoup
from  scholarly import scholarly as scholar
from django.shortcuts import render
from django.views.generic import TemplateView


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

def article_finder_citation(url):
    query = scholar.search_pubs(url)
    x = next(query)
    return x['num_citations']

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

def article_finder_citation(url):
    query = scholar.search_pubs(url)
    x = next(query)
    return x['num_citations']


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

#---------------------------------- ALL PROGRAM ENDS HERE-------------------------------------------------------

# Create your views here.
class HomePageView(TemplateView):
    template_name = "alfa.html"


def alfa_request(request):
    if(request.method == 'POST'):
        x_name= request.POST.get('test_name')
        #return HttpResponse("hello case successfully linked {}".format(x_name))
        list_1 = {1:"alfa"}
        return render(request, 'test.html', {"alfa": list_1}) 


#---------------------------------------------------------------

def hello_world(request):
    if request.method == 'POST':
        article = request.POST.get('test_name')
        try:
           
            #article_11 = article_finder_citation(article)   # provides the citation info'
            article_22 = module(article)   # provides the article info
            abstract_data_1 = abstract_data(article_22[2][1])
            article_aff = affliation_author(article_22[1])
        
            final_data_1 = []
            for i in range(article_22[4]):
                
                    data_13 = final_function(article_22[3][i])
                    final_data_1.append([article_22[3][i],data_13])
                    

            
        except:
            return "Error"
  
           
        # title, doi, download_link, author_names,len_author_names, len_download_link
        return render(request,"summary.html",{"article_name":article_22[0],
        "doi":article_22[1],
        "download_link":article_22[2],
        "author_names":article_22[3],
        "similar_article": final_data_1,
        "abstract_data": abstract_data_1,
        "affliation_data": article_aff[1],
        "publication": article_aff[0]
        })

