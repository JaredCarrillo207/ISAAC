
#Sample Code. Check out https://www.youtube.com/watch?v=Nxu6GlDleqA for a tutorial of sorts.

from pizzapi import *

customer = Customer('Jared', 'Carrillo', 'MY_EMAIL', 'MY_NUMBER')
address = Address('ADDRESS', 'CITY', 'STATE', 'ZIP_CODE')

store = address.closest_store()

order = Order(store, customer, address)
order.add_item('LARGE_DELUXE_PIZZA') 
order.add_item('20BCOKE')  

card = PaymentObject('NUMBER', 'DATE', 'PIN', 'ZIP_CODE')

#Tests order but doesnt actually buy something
order.pay_with(card)