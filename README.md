## Predicting the Opening pirce of Nifty 50.

<p>&nbsp;</p>

### Introduction

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  The Goal of the project is to predict the opening level of the NIFTY 50 based on the sentiment of the news collected after the close of the market till the opening of the market on the next day. In addition to the news sentiment, we would be using other Indices to help us with the prediction.



### Data Source: 

[News Headline Data](https://pulse.zerodha.com/pulse-news-dump.zip) 

The required Index price is pulled from [`yfinance library`](https://pypi.org/project/yfinance/).


<p>&nbsp;</p>
	
### More on the Datasets:
	
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The NewsHeadlines data contains the news headlines from [Pulse](https://pulse.zerodha.com/), a financial news aggregator from [Zerodha](https://zerodha.com/).  The News Headlines Dataset contains the headlines, links and the date and time when it was published. The News headline timeline starts from 2014 and goes on till 2017. but also contain outlier dates, especially from the year 1970. Now coming to stock prices, we would be using `yfinance` module for pulling stock prices. `yfinance` is an API wrapper of yahoo finance, which can be used to pull the necessary data. Since the News data stretches from 2014 to 2017, we'd keep the years 2014 to 2017. 

So, which stock Index are interest in?
1. Nifty 50 (Obsiously):
	Nifty 50 is the benchmark Index used to gauge the National Stock Exchange (NSE). The index consist of 50 Indian listed stocks accounting to 13 important sectors in the National Stock Exchange.  

2. S&P 500 Index:
	S&P 500 is the benchmark Index used to gauge the major US stock exchanges (NASDAQ and NYSE). The Index doesn't have a strict criteria and any inclusion is based on the selection by a committe  S&P Dow Jones Indices. Th committe would assesses the company's merit using eight important critiera i.e Market Capitalzation, Public Float, role of the industry in the economy of the US, Financial Strength, Duration of time in the public market, domicile, liquidity and stock exchange. The Index contains 500 companies. 
	
3. Nikkie 225 Index:
	Nikkie 225 is the Stock index of the Toyko Stock Exchange. The index measures the performance of the top 225 publically traded in the Japanese top stock exchange. 

### Procedure:

1) Getting and Cleaning the Data.
2) Exploratory Analysis.
3) Fitting the Models.
4) Deploying the Model in AWS Lambda. 

#### 1. Getting and Cleaning the Data.

	The News Headline was in the CSV file format, where the Nifty50 Data was in txt format and spread across various folders according to their year. The stock 
      















