import pandas as pd 
import requests, json, time, unicodedata #Requests 2.21.0
from con import sql_con

def deEmojify(inputString):
    returnString = ""
    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            returnString += ''
    return returnString
def is_sampis(string):
    sampis = ['jual', 'wts', 'order']
    for i in sampis:
        if i in sampis:
            return True
    return False
def load_json(link, headers):
    flag = False
    while flag == False:
        try:
            req = requests.get(link, headers, timeout=10)
            flag = True
            time.sleep(0.01)
        except:
            time.sleep(2)
            print('Req. failed. Try again...')
    attemp = 0
    while req.status_code != requests.codes.ok:
        #Gagal
        if attemp < 5:
            req = requests.get(link, headers, timeout=10)
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
        print('sc:', shortcode)
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
    likes_count = root['edge_media_preview_like']['count']
    try:
        conversation = "'"+ root['edge_media_to_caption']['edges'][0]['node']['text'].replace(',','|')
    except:
        conversation = "'"
    location = root['location']
    sampis = is_sampis(conversation)
    if (sampis==False):
        location=''
        shortcode = 'sampah|' + root['shortcode']
    timestamp = root['taken_at_timestamp']
    type_post = root['__typename']
    if type_post=='GraphImage':
        accessibility_caption = root['accessibility_caption']
    else:
        accessibility_caption = ''
    cluster = classifier(accessibility_caption)
    if (location):
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
            'likes_count':likes_count,
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
def main():
    headers = "User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0"
    bucket_clean = []
    bucket_dirty = []

    # print('req...')
    explore_hashtag('exploreindonesia', bucket_dirty, bucket_clean)
    # print('req success')


    tb_clean = sql_con('tb_clean')
    tb_clean.add_data(bucket_clean)
    df = tb_clean.get_df()
    tb_clean.close()

    tb_dirty = sql_con('tb_dirty')
    tb_dirty.add_data(bucket_dirty)
    tb_dirty.close()

    # df['latlng'] = df['lat'] + df['lng']
    df = df.drop_duplicates(subset=['location_id'], keep='last')
    df.to_csv('data.csv',index=False)
    # print('done')
main()