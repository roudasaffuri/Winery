from flask import request, render_template

from userGetWineById import getWineById


def userGetSinglePage(id):
    # best_seller values  1=Bestseller 2=Recommended 3=Favorite
    best_seller = request.args.get('best_seller', default=0, type=int)
    wine = getWineById(id)
    return render_template("userSinglePage.html", wine=wine, best_seller=best_seller)