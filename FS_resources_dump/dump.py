#!/usr/bin/python

import requests

def fetch_place(place_id):
    
    places = []
    
    PLACE_URL='https://www.familysearch.org/service/search/catpl/place'
    r = requests.get('%s/%s' % (PLACE_URL, str(place_id)), headers={'accept': 'application/json'})
    data = r.json()
    print 'Fetch %d %s' % (place_id, data['name'])
    
    i = 0
    here_empty = True
    for link in data['related']:
        
        if link['type'] != 'Child Place':
            continue
        
        _places = fetch_place(link['id'])
        if len(_places) > 0:
            here_empty = False
            places.extend(_places);
        
        i = i + 1
        if i>3:
            break    
    
    if here_empty:
        url = 'https://www.familysearch.org/service/search/cat/v2/search?count=50&placeId=' + str(data['id']) + '&query=%2Bplace%3A%22' + data['name'] + '%22&groupBy=placeSubject' 
        r2 = requests.get(url , headers={'accept': 'application/json'})
        data2 = r2.json()
        # print data2
        
        for searchHit in data2['searchHits']:
            identifier = searchHit['metadataHit']['metadata']['identifier']['value']
            
            url2 = 'https://www.familysearch.org/service/search/cat/search?query=%2Bsubject_id%3A' + str(identifier) + '%20&offset=0&count=50'
            r3 = requests.get(url2 , headers={'accept': 'application/json'})
            data3 = r3.json()
            for searchHit2 in data3['searchHits']:
                
                url4 = searchHit2['metadataHit']['metadata']['identifier']['value']
                microfilms = requests.get(url4, headers={'accept': 'application/json'}).json()
                places.append( (data['name'], url4, microfilms ) )
        
    return places


places = fetch_place(92)
print '-----'
for p in places:
    print [0], p[1]
    if 'film_note' in p[2]['source']:
        for file_note in p[2]['source']['film_note']:
            print file_note
            print str(file_note['filmno'])
            print file_note['text']
            print file_note['digital_film_rights']
            print str(file_note['digital_film_no']), 'https://www.familysearch.org/search/film/%s' % (str(file_note['filmno']))
            
    print ''