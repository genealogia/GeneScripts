#!/usr/bin/python3

import requests
import hashlib
import os
import json

def get_cache(url, headers):
    h = os.path.join('tmp', hashlib.md5(url.encode('utf-8')).hexdigest())
    print('get_cache', h)
    if os.path.exists(h):
        return open(h, 'r').read()
    
    r = requests.get(url, headers=headers)
    f = open(h, 'w')
    content = r.content.decode('utf-8')
    f.write(content)
    f.close()
    
    return content

def print_place(p):
    if 'film_note' in p[2]['source']:
        for file_note in p[2]['source']['film_note']:
            try:
                print(p[0], ';' , p[1], ';',  str(file_note['filmno']), ';', file_note['text'], ';', file_note['digital_film_rights'], ';', str(file_note['digital_film_no']), ';', 'https://www.familysearch.org/search/film/%s' % (str(file_note['filmno'])) )
            except:
                pass

def fetch_place(place_id):
    
    places = []
    
    PLACE_URL='https://www.familysearch.org/service/search/catpl/place'
    #r = requests.get('%s/%s' % (PLACE_URL, str(place_id)), headers={'accept': 'application/json'})
    #data = r.json()
    r = get_cache('%s/%s' % (PLACE_URL, str(place_id)), {'accept': 'application/json'})
    data = json.loads(r)
    #print 'Fetch %d %s' % (place_id, data['name'])
    
    i = 0
    here_empty = True
    for link in data['related']:
        print(link)
        
        if link['type'] != 'Child Place':
            continue
        
        _places = fetch_place(link['id'])
        if len(_places) > 0:
            here_empty = False
            places.extend(_places);
        
        #i = i + 1
        #if i>3:
        #    break    
    
    if here_empty:
        url = 'https://www.familysearch.org/service/search/cat/v2/search?count=50&placeId=' + str(data['id']) + '&query=%2Bplace%3A%22' + data['name'] + '%22&groupBy=placeSubject' 
        #r2 = requests.get(url , headers={'accept': 'application/json'})
        #data2 = r2.json()
        r2 = get_cache(url , headers={'accept': 'application/json'})
        print('!2')
        print(r2)
        data2 = json.loads(r2)
        print('!!2')
        # print data2
        
        for searchHit in data2['searchHits']:
            identifier = searchHit['metadataHit']['metadata']['identifier']['value']
            
            url2 = 'https://www.familysearch.org/service/search/cat/search?query=%2Bsubject_id%3A' + str(identifier) + '%20&offset=0&count=50'
            #r3 = requests.get(url2 , headers={'accept': 'application/json'})
            #data3 = r3.json()
            r3 = get_cache(url2 , headers={'accept': 'application/json'})
            print('!3')
            print(r3)
            data3 = json.loads(r3)
            print('!!3')
            
            for searchHit2 in data3['searchHits']:
                
                url4 = searchHit2['metadataHit']['metadata']['identifier']['value']
                #microfilms = requests.get(url4, headers={'accept': 'application/json'}).json()
                r4 = get_cache(url4, headers={'accept': 'application/json'})
                print('!4')
                print(url4)
                print(r4)
                microfilms = json.loads(r4)
                print('!!4')
                
                if microfilms != {}:
                
                    places.append( (data['name'], url4, microfilms ) )
                    print_place( (data['name'], url4, microfilms ) )
        
    return places


places = fetch_place(92)
print( '-----' )
for p in places:
    print( p[0], p[1] )
    if 'film_note' in p[2]['source']:
        for file_note in p[2]['source']['film_note']:
            try:
                print( str(file_note['filmno']), ';', file_note['text'], ';', file_note['digital_film_rights'], ';' , str(file_note['digital_film_no']), 'https://www.familysearch.org/search/film/%s' % (str(file_note['filmno'])) )
            except:
                print('cos nie tak')
            
    print('')
