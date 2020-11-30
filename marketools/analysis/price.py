

def relative_price_change(new_price: float, ref_price: float):
    """
    Calculates and returns relative price change.

    Parameters
    ----------
    new_price : float
        new/current price
    ref_price : float
        reference price

    Returns
    -------
    float
    """
    
    assert ref_price > 0
    return (new_price - ref_price) / ref_price
