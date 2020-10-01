'''Defines cafe transaction classes.
TODO
Transaction class needs `id` attribute
Basket class needs `id` attribute
Basket class needs `transaction_id` attribute
'''

class RawTransaction:
    '''Describes one transaction from raw csv table.'''
    def __init__(self, date, location, customer_name, basket, pay_amount,
                 payment_method, ccn):
        self.date = date
        self.location = location
        self.customer_name = customer_name
        self.basket = basket
        self.pay_amount = pay_amount
        self.payment_method = payment_method
        self.ccn = ccn
    
    def __repr__(self):
        return f'{self.date}, {self.location}, {self.customer_name}, '\
               f'{self.basket}, {self.pay_amount}, {self.payment_method}, '\
               f'{self.ccn}'

class Transaction:
    '''Describes one customer transaction'''
    def __init__(self, location, customer, datetime, total):
        self.location = location
        self.customer = customer
        self.datetime = datetime
        self.total = total
    
    def __repr__(self):
        return f'{self.location}, {self.customer}, {self.datetime}, {self.total}'

class Basket:
    '''Describes one basket of purchases'''
    def __init__(self, item, cost):
        self.item = item
        self.cost = cost