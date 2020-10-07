class Raw_Transaction:
    def __init__(self, date, location, customer_name, basket, pay_amount,
                 payment_method, ccn, id_number):
        self.date = date
        self.location = location
        self.customer_name = customer_name
        self.basket = basket
        self.pay_amount = pay_amount
        self.payment_method = payment_method
        self.ccn = ccn
        self.id_number = id_number
    
    def __repr__(self):
        return f'{self.date}, {self.location}, {self.customer_name}, '\
               f'{self.basket}, {self.pay_amount}, {self.payment_method}, '\
               f'{self.ccn}, {self.id_number}'

class Transaction:
    def __init__(self, unique_id, date, location, first_name, total, basket):
        self.unique_id= unique_id
        self.date = date
        self.location = location
        self.first_name = first_name
        self.total = total
        self.basket = basket
    
    def __repr__(self):
        return f'{self.unique_id}, {self.date}, {self.location}, {self.first_name}, {self.total}, {self.basket}'

class Raw_Basket:
    def __init__(self, transaction_id, basket_items):
        self.transaction_id = transaction_id
        self.basket_items = basket_items
    
    def __repr__(self):
        return f'{self.transaction_id}: {self.basket_items}'

class Basket:
    def __init__(self, trans_id, item, cost):
        self.trans_id = trans_id
        self.item = item
        self.cost = cost
    
    def __repr__(self):
        return f'{self.trans_id}: {self.item}, {self.cost}'