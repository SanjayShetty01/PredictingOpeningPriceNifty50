## Predicting the Opening price of Nifty 50.

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
2) Pre-Processing the Data
3) Exploratory Analysis.
4) Fitting the Models.
5) Deploying the Model in AWS Lambda. 

#### 1. Getting and Cleaning the Data.

As with any data dataset, finding a raw data ready for analysis is never the case. And our datsets are no expection! So, we would start with News Headlines dataset. The required news headlines data is download from the above website and loaded for cleaning. The News data consisted of fewer data misplacement. Very few of 'Date_Time' consisted of the links or the News headlines. Cleaning of the same is done in the `put the script here` script. 

As mentioned earlier for stock prices, we would be using `yfinance` to load all the required stock prices. So what are the data that interest us?
Before we look into the required data, let's talk about what we would require to build the model. It would be needing the move the US market, the Japanese market and the Indian Market.

So, the data we use for our analysis. 

1.  Closing prices of S&P 500.
2.  Open & Close of Nikkie 225.
3.  Open & Close of NIFTY 50.

#### 2. Pre-Processing the Data

The Headline is passed through the function analzyer_polarity_score() from vaderSentiment moudulues. <put what does it do> The function would return the score in the score in the three columns, i.e. compound, neu(neutral), pos (positive) and neg (negative). 

The formula for compound:



With the sentiment scores figured out, we would now move to add weights to the score. Now why would be interested in adding? And how would we be assigning weights for the same?












