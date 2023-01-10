from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,request
# all functions will be here
from urllib.request import urlopen 
import pandas as pd
from bs4 import BeautifulSoup
from  scholarly import scholarly as scholar
from django.shortcuts import render
from django.views.generic import TemplateView
import numpy as np



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
           
            article_11 = article_finder_citation(article)   # provides the citation info'
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
            return render(request,"partial_info.html",{"article_name":article_22[0],
            "doi":article_22[1],
            "download_link":article_22[2],
            "author_names":article_22[3],
            "abstract_data": abstract_data_1,
            "citation": article_11
            })
  
           
        # title, doi, download_link, author_names,len_author_names, len_download_link
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
def university_lookup(author_name,dict_final):   #dict_final
    try:
        return dict_final[author_name]
    except:
        return ""

#-------------------------------------------------------------
def final_function(name):
    x  = get_article_adv(name)
    y = list(x[x['affliation'] != '']['affliation'])
    t = list(x[x['affliation']!= '']['date'])
    enm = len(y)
    i = 0
    main_keys = []
    main_values = []
    while(i != enm):
        for i1 in y[i]:
            main_keys.append(i1)
        for i2 in t[i]:
            main_values.append(i2)
        i += 1
    dict_final = dict(zip(main_values, main_keys))
    x.dropna(inplace = True)
    x.index = np.arange(len(x['author_list']))
    alfa_list  =[]
    for i in range(len(x['author_list'])):
        for i1 in x['author_list'][i]:
            alfa_list.append([x['publication'][i],pd.to_datetime(x['date'][i]),x['title'][i],i1])
    
    final_dataset = pd.DataFrame(alfa_list,columns=['publication','date','title','author'])
    final_dataset['affiliation'] = final_dataset['author'].apply(university_lookup,args = ([dict_final]))
    final_dataset['author_lower']  = final_dataset['author'].apply(lambda x: x.lower())
    list_1 = final_dataset['title']
    list_2 = final_dataset['author_lower']
    set_1 = list(zip(list_1, list_2))
    html_code = []
    for i in set_1:
        html_code.append("<form action = '/adv_details' method = 'get'><input type = 'hidden' name= 'hidden_value' value = '{} {}'><input type = 'submit' value = 'article_details'></form>".format(i[1],i[0]))
    final_dataset['link'] = np.array(html_code)

    return final_dataset



# ==============================================================================

# manager
def manage_adv(request):
    if request.method == 'POST':

        article = request.POST.get('author_name')
        try:
            data_1 = final_function(article)
            return HttpResponse(data_1.to_html(escape=False))

        except:
            return HttpResponse("error")
# handling advanced request


def hello_world_adv(request):
        if request.method == 'GET':
            article = request.GET.get('hidden_value')
            try:
                article_11 = article_finder_citation(article)   # provides the citation info'
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

