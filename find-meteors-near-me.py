import requests, math

meteor_resp=requests.get("https://data.nasa.gov/resource/gh4g-9sfh.json")
meteor_resp_json=meteor_resp.json()


def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

my_loc = (18.520760, 73.855408)


for meteor in meteor_resp_json:
    if not ('reclat' in meteor and 'reclong' in meteor):
        continue
    meteor['dist']=calc_dist(float(meteor['reclat']), float(meteor['reclong']), my_loc[0], my_loc[1])


def get_dist(meteor):
    return meteor.get('dist', math.inf)

meteor_resp_json.sort(key=get_dist)

nearestTen = meteor_resp_json[0:10]
print("Nearest 10 Meteors:", nearestTen)

farthestTen = meteor_resp_json[-1:-11:-1]
print("Farthest 10 Meteors:", farthestTen)

withoutLocData = len([m for m in meteor_resp_json if 'dist' not in m]) 
print(withoutLocData, "Meteors are without location data")