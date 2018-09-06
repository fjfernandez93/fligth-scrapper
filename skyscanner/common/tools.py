

def parse_currency_to_eur(quantity, currency):
    """
    Translate a given quantity of a determinate currency to its equivalent in euros.
    :param quantity: quantity of the currency
    :param currency: the indentifier of the currency
    :return: the quantity in euros
    """
    euros = -1
    if currency == 'zł':
        euros = quantity * 0.23
    return round(euros, 2)