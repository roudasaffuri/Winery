class Wine:
    def __init__(self, id, wine_name, wine_type, image_url, price, stock, description, best_before, product_registration_date, discount, final_price):
        self.id = id
        self.wine_name = wine_name
        self.wine_type = wine_type
        self.image_url = image_url
        self.price = price
        self.stock = stock
        self.description = description
        self.best_before = best_before
        self.product_registration_date = product_registration_date
        self.discount = discount
        self.final_price = final_price
    def __repr__(self):
        return f"Wine(id={self.id}, wine_name={self.wine_name}, wine_type={self.wine_type}, price={self.price},discount={self.discount})"
