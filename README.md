## Predicting the Opening pirce of Nifty 50.

<p>&nbsp;</p>

### Introduction

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
One of the interesting and most abundantly found data can be from the stock market. Moreover, it could also be financially lucrative, as a strong-predictive model with phenomenal output could result in one owning a 'money printing machine'. The NewsHeadlines data contains the news headlines from [Pulse](https://pulse.zerodha.com/), a financial news aggregator from [Zerodha](https://zerodha.com/). 



### Data Source: 

[News Headline Data](https://pulse.zerodha.com/pulse-news-dump.zip) 

The required Index price is pulled from [`yfinance library`](https://pypi.org/project/yfinance/).


<p>&nbsp;</p>
	
### More on the Datasets:
	
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The News Headlines Dataset contains the headlines, links and the date and time when it was published. The News headline timeline starts from 2014 and goes on till 2017. but also contain outlier dates, especially from the year 1970. Now coming to stock prices, we would be using `yfinance` module for pulling stock prices. `yfinance` is an API wrapper of yahoo finance, which can be used to pull the necessary data. Since the News data stretches from 2014 to 2017, we'd keep the years 2014 to 2017. 

So, which stock Index are interest in?
1. Nifty 50 (Obsiously):
	Nifty 50 is the benchmark Index used to gauge the National Stock Exchange (NSE). The index consist of 50 Indian listed stocks in the National Stock Exchange.  

2. S&P 500 Index:
	S&P 500 is the benchmark Index used to gauge the major US stock exchanges (NASDAQ and NYSE).
	
3. Nikkie 225 Index

### Procedure:

1) Getting the Data.
2) Cleaning the Data.
3) Exploratory Analysis.
4) Fitting the Models.
5) Deploying the Model in AWS Lambda. 

#### 1. Getting the Data














