from marketools.wallet import Commission


def test_commission__trade_below_min():
    com = Commission(0.01, 3)
    assert 3 == com(250)


def test_commission__trade_above_min():
    com = Commission(0.01, 3)
    assert 5.5 == com(550)


def test_commission__trade_at_min():
    com = Commission(0.01, 3)
    assert 3 == com(300)


def test_commission__minimal_recommended_investment():
    com = Commission(0.002, 3.0)
    assert 1500 == com.minimal_recommended_investment()


def test_commission__minimal_recommended_investment__zero_minimum():
    com = Commission(0.01, 0.0)
    assert 0 == com.minimal_recommended_investment()
