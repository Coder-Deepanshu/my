import pandas as pd

amount=int(input('Enter Amount :'))
currency=str(input('Enter Currency type:'))
dict1={'Australia':83.5,'Eurozone':91.0,'United Kingdom':108.5,'United Arab Emirates':22.7}

while amount>0:
    if currency=='USD':
        print(f'RS.{dict1['Australia']*amount}')
        break
    elif currency=='EUR':
        print(f'RS.{dict1['Eurozone']*amount}')
        break
    elif currency=='GBP':
        print(f'RS.{dict1['United Kingdom']*amount}')
        break
    elif currency=='AED':
        print(f'RS.{dict1['United Arab Emirates']*amount}')
        break