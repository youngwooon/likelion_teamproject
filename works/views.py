from django.shortcuts import render
import googlemaps # pip install googlemaps
import pprint # pip install prettyprint
import time
import random
from keras.models import load_model # pip install tensorflow
from PIL import Image, ImageOps
# from keras.saving.saving_utils import trace_model_call # pip install pillow
import numpy as np # pip install numpy
import requests
import concurrent.futures
import imagehash # pip install imagehash

from works.models import PlaceInfo, Food, NoFood

my_api_key='AIzaSyAzbAG3wZN7pS2i0Dzs9MNzdqSfY7fvQF8'
gmaps = googlemaps.Client(key=my_api_key)

def get_food_refs(request):
    global raw_data
    global food_refs
    raw_data = {}
    food_refs = {}
    # 입력받은 변수
    global origin_lat
    global origin_lng
    origin_lat = request.POST['latitude']
    origin_lng = request.POST['longitude']
    input_location = f'{origin_lat}, {origin_lng}'
    input_radius = request.POST['radius']
    input_round = int(request.POST['round'])

    # 1. place id 수집
    ten_random_place_ids = get_ten_random_place_ids(input_location, input_radius, input_max_price=None, input_open_now=None)
    pprint.pprint(ten_random_place_ids)
    print(len(ten_random_place_ids))

    # 2. photo refs 수집 및 셔플
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(save_photo_refs, ten_random_place_ids)
    photo_refs_all = sum(raw_data.values(), [])
    random.shuffle(photo_refs_all)
    print(photo_refs_all)
    print(len(photo_refs_all))

    # 3. 음식사진 선별하여 저장

    #### 1개씩 선별하는 경우 ####
    # save_food_refs(photo_refs_all, input_round)

    #### 2개 이상씩 선별하는 경우 (Thread) ####
    with concurrent.futures.ThreadPoolExecutor() as executor:
        split_num = round(len(photo_refs_all)/2)
        arguments = [[photo_refs_all[:split_num], photo_refs_all[split_num:]],
            [input_round,input_round]]
        executor.map(save_food_refs, *arguments)
    
    # 4. 결과값 변수에 지정
    new_food_refs = dict(list(food_refs.items())[0:input_round])
    first_img_ref = list(new_food_refs.keys())[0]
    second_img_ref = list(new_food_refs.keys())[-1]
    context = {
        'result': new_food_refs,
        'first_img_ref': first_img_ref,
        'second_img_ref': second_img_ref
    }
    return render(request, 'works/choice.html', context)

def result(request):
    selected_photo_ref = request.POST['selected_photo_ref']
    for key, value in raw_data.items():
        if selected_photo_ref in value:
            selected_place_id = key
    destination_lat = PlaceInfo.objects.get(place_id=selected_place_id).lat
    destination_lng = PlaceInfo.objects.get(place_id=selected_place_id).lng
    name = PlaceInfo.objects.get(place_id=selected_place_id).name
    context = {
        'origin_lat': origin_lat,
        'origin_lng': origin_lng,
        'destination_lat': destination_lat,
        'destination_lng': destination_lng,
        'name': name
    }
    return render(request, 'works/result.html', context)

def get_ten_random_place_ids(input_location, input_radius, input_max_price=None, input_open_now=None):
    place_ids = []
    places_result = gmaps.places_nearby(
        location=input_location,
        radius = input_radius,
        max_price = input_max_price,
        open_now = input_open_now,
        type = 'restaurant'
    )
    
    #### 첫 페이지만 수집하는 경우 (최대 20개 장소) ####
    for place in places_result['results']:
        place_ids.append(place['place_id'])

    #### 모든 페이지 수집하는 경우 (최대 60개 장소) ####
    # while True:
    #     for place in places_result['results']:
    #         place_ids.append(place['place_id'])
    #     # 검색 결과가 20개 이상인 경우 다음 페이지 수집 / 로딩 시간 위한 시간 공백 설정
    #     time.sleep(2)
    #     if 'next_page_token' in list(places_result.keys()):
    #         places_result = gmaps.places_nearby(page_token = places_result['next_page_token'])
    #         continue
    #     else:
    #         break

    ten_random_place_ids = random.sample(place_ids, 10)
    return ten_random_place_ids

def save_photo_refs(my_place_id):
    my_fields = ['name', 'photo', 'geometry/location/lat', 'geometry/location/lng']
    place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
    place_id = my_place_id
    name = place_details['result']['name']
    lat = place_details['result']['geometry']['location']['lat']
    lng = place_details['result']['geometry']['location']['lng']
    PlaceInfo.objects.update_or_create(place_id=place_id, name=name, lat=lat, lng=lng)

    photo_refs = []
    raw_data[my_place_id] = photo_refs
    try:
        for photo in place_details['result']['photos']:
            photo_refs.append(photo['photo_reference'])
    except:
        pass

# teachable machine
def is_food(photo_ref):
    model = load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(requests.get(f'https://maps.googleapis.com/maps/api/place/photo?photoreference={photo_ref}&maxwidth=600&key={my_api_key}', stream=True).raw)
    hash = imagehash.average_hash(image)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    if Food.objects.filter(photo_hash=hash).exists():
        prediction = True
        print("모델 FOOD")
    elif NoFood.objects.filter(photo_hash=hash).exists():
        prediction = False
        print("모델 NOFOOD")
    elif model.predict(data)[0][0] >= 0.9:
        Food.objects.update_or_create(photo_hash=hash)
        prediction = True
        print("FOOD")
    else:
        NoFood.objects.update_or_create(photo_hash=hash)
        prediction = False
        print("NOFOOD")
    return prediction

def save_food_refs(photo_refs_all, round):
    for photo_ref in photo_refs_all:
        if len(food_refs) >= round:
            break
        else:
            try:              
                if is_food(photo_ref):
                    for key, value in raw_data.items():
                        if photo_ref in value:
                            food_refs[photo_ref] = key
                            print(f'수집한 음식사진 개수: {len(food_refs)}')
                else:
                    pass
            except:
                pass
