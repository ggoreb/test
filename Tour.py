class TourInfo:
    def __init__(self, title, price, area, link, img):
        self.title = title
        self.price = price
        self.area = area
        self.link = link
        self.img = img

    def __str__(self):
        return self.title + ' ' + self.price + ' ' + self.area + ' ' + self.link + ' ' + self.img
