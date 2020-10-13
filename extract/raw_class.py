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