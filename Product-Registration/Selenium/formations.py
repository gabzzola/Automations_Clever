def format_price(price):
    if isinstance(price, str):
        price = float(price.replace(',', '.'))
    return f'{price:.2f}'.replace('.', ',')