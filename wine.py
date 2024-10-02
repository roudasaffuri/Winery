import requests
# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR WINE.
# https://www.npoint.io/ to build OWN API
# wines = requests.get("https://api.npoint.io/e92c93ac5012d4a6a315").json()


class Wine:
    def __init__(self, img, price, title, country, province, description):
        self.img = img
        self.price = price
        self.title = title
        self.country = country
        self.province = province
        self.description = description

    def __str__(self):
        return f"{self.title} from {self.province}, {self.country} - Price: ${self.price}"


def get_wines():
    total_wines = []
    wines = requests.get("https://api.npoint.io/e92c93ac5012d4a6a315").json()
    print(wines)
    for w in wines:
        wine = Wine(w['img'], w['price'], w['title'], w['country'], w['province'], w['description'])
        total_wines.append(wine)
    return total_wines

