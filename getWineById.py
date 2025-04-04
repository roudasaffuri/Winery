from flask import render_template
from getProductByID import get_wine_by_id

def getWineById(id):
    wine = get_wine_by_id(id)
    if wine:
        return render_template("singlePage.html", wine=wine)
    else:
        return "Product not found", 404