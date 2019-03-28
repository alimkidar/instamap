import pandas as pd
import requests, json, time, unicodedata
from con import sql_con

headers = "User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"
def deEmojify(inputString):
    returnString = ""
    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            returnString += ''
    return returnString

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
def explore_hashtag(tag, bucket_dirty, bucket_clean):
    url_tags = 'https://www.instagram.com/explore/tags/'+tag+'/?__a=1'
    data_tags = load_json(url_tags, headers)
    edges = data_tags['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    for edge in edges:
        shortcode = edge['node']['shortcode']
        print(shortcode)
        url_sc = 'https://www.instagram.com/p/'+shortcode+'/?__a=1'
        data_sc = load_json(url_sc, headers)
        lokasi = data_sc['graphql']['shortcode_media']['location']
        if (lokasi):
            data = open_post(data_sc)
            bucket_clean.append(data[0])
        bucket_dirty.append({'hashtag':tag, 'shortcode':shortcode})

def classifier(accessibility_caption): # TODO: buat klasifikasi foto
    string = accessibility_caption.lower()
    cluster = ['mountain', 'people', 'beach', 'ocean']
    x = 'other'
    for i in cluster:
        if i in string:
            x = i
    return x

def open_post(data):
    bucket = []
    try:
        root = data['graphql']['shortcode_media']
    except:
        # print(data)
        return print("error:")
    username = root['owner']['username']
    display_url = root['display_url']
    height = root['dimensions']['height']
    width = root['dimensions']['width']
    shortcode = root['shortcode']
    try:
        conversation = "'"+ root['edge_media_to_caption']['edges'][0]['node']['text'].replace(',','|')
    except:
        conversation = "'"
    timestamp = root['taken_at_timestamp']
    type_post = root['__typename']
    if type_post=='GraphImage':
        accessibility_caption = root['accessibility_caption']
    else:
        accessibility_caption = ''
    cluster = classifier(accessibility_caption)
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
            'height': height,
            'width': width,
            'shortcode':shortcode,
            'conversation': deEmojify(conversation),
            'timestamp': timestamp,
            'accessibility_caption': accessibility_caption,
            'location_id':location_id,
            'location_name':deEmojify(location_name),
            'lat': lat,
            'lng': lng,
            'count':count,
            'url_loc': 'https://www.instagram.com/explore/locations/'+location_id+'/',
            'url_post': 'https://www.instagram.com/p/'+shortcode+'/',
            'cluster':cluster
        })
    return bucket
bucket_clean = []
bucket_dirty = []

print('req')
explore_hashtag('exploreindonesia', bucket_dirty, bucket_clean)
print('req success')


tb_clean = sql_con('tb_clean1')
tb_clean.add_data(bucket_clean)
df = tb_clean.get_df()

tb_dirty = sql_con('tb_dirty1')
tb_dirty.add_data(bucket_dirty)

df['latlng'] = df['lat'] + df['lng']
df = df.drop_duplicates(subset=['latlng'], keep='last')
df.to_csv('data.csv',index=False)
print('done')