

def relative_price_change(new_price, ref_price):
    assert ref_price > 0
    return (new_price - ref_price) / ref_price
