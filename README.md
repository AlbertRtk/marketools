marketools: tools for stock market analysis
===========================================

[![PyPI Latest Release](https://img.shields.io/pypi/v/marketools.svg)](https://pypi.org/project/marketools/)
[![License](https://img.shields.io/pypi/l/marketools.svg)](https://github.com/AlbertRtk/marketools/blob/main/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/marketools.svg)]()

## About
marketools is a Python package for web scraping and analysis of stock market data. Project is under development. At the moment, analysis functionality is limited. You are welcomed to contribute to the project.

### Source of data
Data are scraped from [Stooq](http://stooq.com/) service.

## Support
You may report issues and functionality requests [here](https://github.com/AlbertRtk/marketools/issues).

## Installation
```bash
pip install marketools
```
or 
```bash
git clone https://github.com/AlbertRtk/marketools.git
```

## Documentation
* [Documentation](https://albertrtk.github.io/marketools/docs/html/marketools/index.html)
    * [analysis](https://albertrtk.github.io/marketools/docs/html/marketools/analysis/index.html)
    * [stock](https://albertrtk.github.io/marketools/docs/html/marketools/stock.html)
    * [stqscraper](https://albertrtk.github.io/marketools/docs/html/marketools/stqscraper/index.html)

## Example
Import Stock class
```python
from marketools import Stock
```
Create Stock instance for selected ticker, here [PKN](https://stooq.com/q/?s=pkn)
```python
pkn = Stock('PKN')
```
For not Polish stocks, you need to append country code to the ticker (after a dot), e.g.,
```python
apple = Stock('AAPL.US')
```
Get and print OHLC (open-high-low-close) data from the last 5 days
```python
pkn_ohlc = pkn.ohlc  # returns pandas.DataFrame
print(pkn_ohlc.tail(5))
```
Print available fundamental information
```python
print(pkn.fundamentals)
```
