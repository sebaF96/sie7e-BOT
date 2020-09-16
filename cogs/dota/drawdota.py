from PIL import Image, ImageDraw
from io import BytesIO
from constants import Fetcher
import requests
import json


def fetch_items():
    response = requests.get(Fetcher.DOTACONSTANTS_ITEMS_URL.value)
    full_items_dict = json.loads(response.text)
    min_items_dict = {}
    base_url = Fetcher.HEROPICTURE_BASE_URL.value
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

    result.thumbnail((result.size[0] * 0.6, result.size[1] * 0.6), Image.ANTIALIAS)
    result.save("cogs/dota/last_match_items.png")
    return result


def paste_image(image1, image2, x, y):
    temp_image = Image.new("RGBA", image1.size)
    temp_image.paste(image2, (x, y))
    return Image.alpha_composite(image1, temp_image)


def dota_rank_icon(rank_tier: int):
    filename = 'cogs/dota/last_medal.png'
    if rank_tier is None:
        rank_tier = 0

    badge_num = rank_tier // 10
    stars_num = min(rank_tier % 10, 7)

    image = Image.open(f"cogs/dota/images/rank_{badge_num}.png")

    if stars_num > 0:
        stars_image = Image.open(f"cogs/dota/images/stars_{stars_num}.png")
        image = paste_image(image, stars_image, 0, 0)

    image.save(filename, "png")
    return image
