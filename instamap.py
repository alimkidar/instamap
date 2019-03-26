import pandas as pd
import requests, json, time

headers = "User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"

def load_json(link, headers):
    flag = False
    while flag == False:
        try:
            req = requests.get(link, headers)
            flag = True
            time.sleep(0.01)
        except:
            time.sleep(2)
            print('Req. failed. Try again...')
    attemp = 0
    while req.status_code != requests.codes.ok:
        #Gagal
        if attemp < 5:
            req = requests.get(link, headers)
        else:
            req = 0
            break
    if req.status_code == requests.codes.ok:
        x = json.loads(req.text)
        # print ("OK.")
    else:
        x = 0
    return x
def explore_hashtag(tag):
    bucket = []
    url_tags = 'https://www.instagram.com/explore/tags/'+tag+'/?__a=1'
    data_tags = load_json(url_tags, headers)
    edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    for edge in edges:
        shortcode = edge['node']['shortcode']
        url_sc = 'https://www.instagram.com/p/'+sc+'/?__a=1'
        data_sc = load_json(url_sc, headers)
        lokasi = data_sc['graphql']['shortcode_media']['location']
        if (lokasi):
            url_loc = 'https://www.instagram.com/explore/locations/'+lokasi+'/?__a=1'
            data_loc = load_json(url_loc, headers)
            open_post(data_loc, bucket)

def classifier(accessibility_caption): # TODO: buat klasifikasi foto
    string = accessibility_caption.lower()
    if 'mountain' in string:
        x = 'mountain'
def open_post(data, bucket):
    root = data['graphql']['shortcode_media']
    username = root['owner']['username']
    display_url = root['display_url']
    hight = root['dimensions']['hight']
    width = root['dimensions']['width']
    shortcode = root['shortcode']
    try:
        conversation = "'"+ root['edge_media_to_caption']['edges'][0]['node']['text'].replace(',','|')
    except:
        conversation = "'"
    timestamp = root['taken_at_timestamp']
    type_post = root['__typename']
    if type_post=='GraphImage':
        accessibility_caption = ['accessibility_caption']
    else:
        accessibility_caption = ''

    if (root['location']):
        location_id = str(root['location']['id'])
        location_name = root['location']['name']
        url_loc = 'https://www.instagram.com/explore/locations/'+location_id+'/?__a=1'
        data_loc = load_json(url_loc, headers)
        lat = data_loc['graphql']['location']['lat']
        lng = data_loc['graphql']['location']['lng']
        count = data_loc['graphql']['location']['edge_location_to_media']['count']
        bucket.append({
            'username':username,
            'display_url': display_url,
            'hight': hight,
            'width': width,
            'shortcode':shortcode,
            'conversation': conversation,
            'timestamp': timestamp,
            'accessibility_caption': accessibility_caption,
            'location_id':location_id,
            'location_name':location_name,
            'lat': lat,
            'lng': lng,
            'count':count,
            'url_loc': 'https://www.instagram.com/explore/locations/'+location_id+'/',
            'url_post': 'https://www.instagram.com/p/'+shortcode+'/'
        })
