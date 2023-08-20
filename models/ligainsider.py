import requests # Scrape Bundesliga fixtures
import lxml.html as lh # Scrape Bundesliga fixtures

'''
This scraps Ligainsider
'''

def ligainsider_scraper():
    ligainsider = 'https://www.ligainsider.de/stats/kickbase/rangliste/feldspieler/durchschnitt/' # old https://www.ligainsider.de/stats/kickbase/marktwerte/gesamt/
    page_player_information = requests.get(ligainsider) #Create a handle, page, to handle the contents of the website

    doc = lh.fromstring(page_player_information.content) #Store the contents of the website under doc

    tr_elements = doc.xpath('//tr') #Parse data that are stored between <tr>..</tr> of HTML


    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))


    #Since our first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
        #If row is not of size 8, the //tr data is not from our table 
        if len(T)!=9:
            break
        
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1


    ligainsider_Dict={title:column for (title,column) in col}

    return ligainsider_Dict