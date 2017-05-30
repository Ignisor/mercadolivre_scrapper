import mongoengine

mongoengine.connect('mercadolivre', 'default')


class Product(mongoengine.Document):
    url = mongoengine.URLField(unique=True)

    name = mongoengine.StringField(max_length=256)
    category = mongoengine.StringField(max_length=256)
    subcategory = mongoengine.StringField(max_length=256)

    price = mongoengine.FloatField()
