class Spice:
    """this is a spice... hopefully it is not too spicy :)"""

    def __init__(self, init_id, init_name, init_category, init_in_stock):
        self.id = init_id
        self.name = init_name
        self.category = init_category
        self.in_stock = init_in_stock

    def __str__(self):
        return f"Spice(id={self.id}, name='{self.name}', category='{self.category}', in_stock={self.in_stock})"