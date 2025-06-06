# https://www.npoint.io/   to create API
# demo urlEndPointTipsJson = "https://api.npoint.io/9e5a10a7b6fe21ba98aa"

import requests

urlEndPointTipsJson = "https://api.npoint.io/12c67fcd86986ce5cb43"

class WineTip:
    def __init__(self, number, tip, text, image):
        self.number = number
        self.tip = tip
        self.text = text
        self.image = image

def get_wine_tips():
    wine_tips_list = []
    response = requests.get(urlEndPointTipsJson).json()

    # Extract tips and title from the JSON
    tips = response["wine_tips"]["tips"]

    for tip in tips:
        wine_tip = WineTip(tip['number'], tip['tip'], tip['text'], tip['image'])
        wine_tips_list.append(wine_tip)

    return wine_tips_list

