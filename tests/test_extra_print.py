from marketools.extra_print import print_green, print_red, \
    determine_print_color_from_prices


def test_determine_print_color_from_prices__green():
    result = determine_print_color_from_prices(12.3, 9)
    assert print_green == result


def test_determine_print_color_from_prices__red():
    result = determine_print_color_from_prices(0.5, 0.9)
    assert print_red == result


def test_determine_print_color_from_prices__red_eq():
    result = determine_print_color_from_prices(3, 3)
    assert print_red == result
