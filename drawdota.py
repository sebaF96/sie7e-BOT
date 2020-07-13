from PIL import Image
import requests
from io import BytesIO
import json


def fetch_items():
    with open("items.json", "r") as file:
        full_items_dict = json.loads(file.read())
        min_items_dict = {}
        base_url = "https://steamcdn-a.akamaihd.net"
        for item in full_items_dict:
            min_items_dict[full_items_dict[item]["id"]] = base_url + full_items_dict[item]["img"]

        return min_items_dict


ITEMS_DICT = fetch_items()


def get_url_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def get_item_image(item_id):
    try:
        return get_url_image(ITEMS_DICT[item_id])
    except KeyError:
        return Image.new('RGBA', (10, 10), (0, 0, 0, 0))


def save_build_image(build):
    build.sort(reverse=True)
    images = []
    item_size = (88, 64)

    for i in range(0, 6):
        item = build[i]
        if item:
            images.append(get_item_image(item))
        else:
            images.append(Image.new("RGBA", item_size))

    widths, heights = zip(*(i.size if i else item_size for i in images))
    result = Image.new("RGBA", (sum(widths), max(heights)))

    x = 0
    for i in range(len(images)):
        result.paste(images[i], (x, 0))
        x += item_size[0]

    result.save("last_match_items.png")
    return result