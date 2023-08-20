import requests # Scrape Bundesliga fixtures
import lxml.html as lh # Scrape Bundesliga fixtures
import pandas as pd

'''
This scraps performance index data from liga insider
'''

def performance_index():
    performance_index = 'https://www.ligainsider.de/bundesliga/noten/'
    page_player_information = requests.get(performance_index) #Create a handle, page, to handle the contents of the website

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
        if len(T)!=10:
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


    performance_index={title:column for (title,column) in col}
    performance_index=pd.DataFrame(performance_index)
    performance_index=performance_index[['Spieler','Ø–Note Gesamt','Ø–Min. Gesamt']]

    performance_index['Spieler'] = [x.replace('\n', '') for x in performance_index['Spieler']] #removes /n 
    performance_index['Spieler'] = performance_index['Spieler'].astype(str)

    performance_index['Ø–Note Gesamt'] = [x.replace('\n', '') for x in performance_index['Ø–Note Gesamt']] #removes /n 
    performance_index['Ø–Note Gesamt'] = [x.replace(',', '.') for x in performance_index['Ø–Note Gesamt'].astype(str)] #replace commas with dots

    performance_index['Ø–Note Gesamt'] = performance_index['Ø–Note Gesamt'].astype(float)

    return performance_index
