from classes import Raw_Transaction, Transaction, Raw_Basket, Basket
# from datetime import date

# def get_date():
#     today = date.today()
#     d = today.strftime("%m/%d/%y")
#     return(d)
    
def clean_transactions(raw_transaction_list):
    '''Returns a list of clean transactions.'''
    clean_transaction_list = []
    for raw_transaction in raw_transaction_list:
        # Convert datetime to 'month-day-year hh:ss' format'
        date, time = raw_transaction.date.split(maxsplit=1)
        day, month, year = date.split('/')
        clean_date = f'{month}-{day}-{year}'
        # Create unique ID
        abbreviated_location = raw_transaction.location[:4].upper()
        id_string = f'{clean_date}-{abbreviated_location}-{raw_transaction.id_number}'
        # Remove surname
        name = raw_transaction.customer_name.split()[0]
        # Create clean transaction and append to list
        clean_transaction = Transaction(
            unique_id=id_string,
            date=f'{clean_date} {time}',
            location=raw_transaction.location,
            first_name=name,
            total=float(raw_transaction.pay_amount),
            basket=raw_transaction.basket
        )
        clean_transaction_list.append(clean_transaction)
    return clean_transaction_list

def update_raw_basket(clean_transaction_list):
    '''Returns list of raw baskets.'''
    raw_basket_list = []
    for transaction in clean_transaction_list:
        transaction_id = transaction.unique_id
        basket = transaction.basket.replace("\"", "")
        items = basket.split(",")
        for item in items:
            combined_basket = Raw_Basket(transaction_id = transaction_id, basket_items = item)
            raw_basket_list.append(combined_basket)
    return raw_basket_list
          
def clean_basket_items(raw_basket_list):
    '''Cleans list of raw baskets.'''
    clean_basket_list = []
    for sale in raw_basket_list:
        identifier = sale.transaction_id
        order = sale.basket_items
        item, cost = order.rsplit("-", 1)
        basket_item = Basket (trans_id = identifier,
                              item = item,
                              cost = cost)
        clean_basket_list.append(basket_item)
    return clean_basket_list
        