# https://www.npoint.io/   to create API

import requests

urlEndPointTipsJson = "https://api.npoint.io/9e5a10a7b6fe21ba98aa"
class WineTip:
    def __init__(self, number, tip, image):
        self.number = number
        self.tip = tip
        self.image = image


def get_wine_tips():
    wine_tips_list = []
    response = requests.get(urlEndPointTipsJson).json()

    for tip in response["wine_tips"]:
        wine_tip = WineTip(tip['number'], tip['tip'], tip['image'])
        wine_tips_list.append(wine_tip)

    return wine_tips_list


