def format_price(price):
    price = float(price.replace(',', '.'))
    return f'{price:.2f}'.replace('.', ',')