import math
import requests
from PIL import Image
import sys

def deg2num(lat_deg, lon_deg, zoom):
  '''recupération des coordonnées pour avoir la tuile'''
  lat_rad = math.radians(lat_deg)
  n = 1 << zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return xtile, ytile

def getimg(xtile, ytile, zoom):
    '''recupération d'image'''
    url = f"https://tile.openstreetmap.org/{zoom}/{xtile}/{ytile}.png"
    headers = {
    "User-Agent": "Sae n*15"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("image.jpg", "wb") as f:
            f.write(response.content)
        print("Image téléchargée")
    else:
        print("Erreur :", response.status_code)

def defimg(lat, lon, zoom):
    coord = {
        "lat": [lat-1, lat, lat+1],
        "lon": [lon-1, lon, lon+1],
    }
    headers = {
        "User-Agent": "Sae n*15"
    }

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][0]}/{coord['lon'][0]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageHG.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][1]}/{coord['lon'][0]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageHC.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][2]}/{coord['lon'][0]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageHD.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][0]}/{coord['lon'][1]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageCG.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][1]}/{coord['lon'][1]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageC.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][2]}/{coord['lon'][1]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageCD.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][0]}/{coord['lon'][2]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageBG.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][1]}/{coord['lon'][2]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageBC.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)

    url = f"https://tile.openstreetmap.org/{zoom}/{coord['lat'][2]}/{coord['lon'][2]}.png"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("imageBD.jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Erreur :", response.status_code)


def assemblimg():
    images_paths = [
        "imageHG.jpg", "imageHC.jpg", "imageHD.jpg",
        "imageCG.jpg", "imageC.jpg", "imageCD.jpg",
        "imageBG.jpg", "imageBC.jpg", "imageBD.jpg"
    ]
    images = [Image.open(img) for img in images_paths]
    w, h = images[0].size
    final_img = Image.new("RGB", (w * 3, h * 3))
    for i, img in enumerate(images):
        x = (i % 3) * w
        y = (i // 3) * h
        final_img.paste(img, (x, y))
    final_img.save("neufXneufIMG.png")

def getimgcoord(lat_deg, lon_deg, zoom):
    xtile,ytile = deg2num(lat_deg,lon_deg,zoom)
    defimg(xtile, ytile,zoom)
    assemblimg()

if __name__ == '__main__' :
    if len(sys.argv) == 4:
        lat = float(sys.argv[1]) # Conversion texte -> nombre
        lon = float(sys.argv[2])
        zoom = int(sys.argv[3])
        getimgcoord(lat, lon, zoom)

