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

Let us start with the latter question, the weights were assigned based on the published time of the particular news headline. Now coming back on the why we are doing so?
	
The rationale behind assigning weights to News or a piece of new information is an assumption that any News published way before the market opens would be scrutinized and analyzed in a manner that the panic initially created by the News would subside. Thereby nullifying the absolute effect on the market open. Hence to capture such actions, it would be beneficial to use weights.  


The data provided by the yfinace has no issues. Therefore we could safely assume that the data provided is accurate. But we shall be removing some columns, which render useless to our analysis. After removing the unnecessary, we could proceed to process our data as per the model requirement.

#### Why are we using the S&P500 & Nikkie Index??
The US markets usually decides the tempo for the rest of the financial markets around the globe, which was solidified by the high correlation between the S&P500 and the Nifty50. 
And coming to the Nikkie 225, the Japanese market also influences the Indian market. (due to a presence of co-integration and co-movement) [TESTING FINANCIAL INTEGRATION BETWEEN STOCK MARKET OF
INDIA AND JAPAN: AN EMPIRICAL STUDY](https://www.srcc.edu/system/files/TESTING.pdf)

- `USMove`: Stores the S&P500 closing price difference.

- `JapanGap`: Stores the difference between the previous day closing price and the Opening prices. 


#### 3) Exploratory Analysis.
#### 4) Fitting the Models.	
	
	
#### 5) Deploying the Model in AWS Lambda. 
	
So we have fitted and choosen a model. Hence we move to deploying the model. We could connect the model with the Broker API, make a trading bot and live test the performance. But since the broker APIs are kind of expensive. We would deploy model in the cloud and live test the performance. To accomplish the same, We would need a program that would extract the required finance data from Yahoo Finance and the News data from the News API. The data would pass through the model, and the output from the model would store the result in the .csv file. 

How can we come about doing the same?
- We can set up a cronjob in our local machine.
- We can schedule a Github Workflow Action. 
- We can use a Cloud Service.

I’ll be choosing the cloud service (AWS) over the other choices because I would like to familiarize myself with Cloud Computing. 	
	
### How are we going to deploy the same in AWS?
Since the current application (model) needs to run at just a specific time of the day. Hence we could use AWS Lambda (write about AWS Lambda stuff).
 
But AWS lambda has some cons with respect to our project: 

1. Lambda function requires an additional package (Other than the default packages provided by python 3.9).

2. The lambda function needs internet connectivity.	
	

##### How can we solve the package issue?
There are many ways to install external packages in the lambda function,

We bundle the whole code and packages in a zip file and upload it to the lambda function.
We run the pip install code in our code and provide the host machines temp file as a path to install the packages. 
We could upload the packages as Layers in AWS Lambda. 
We can use the EFS file system to store the packages and mount the same to our lambda function.

We would be using the EFS functions, but why?
The reason for choosing the EFS file system is that the packages required for deploying our model were well over 600 MB. Since the limit for ZIP files and Layers are 250 MB (when unzipped). Running the temp file would also hinder the performance since all the packages need to be downloaded and installed on each run, hence could result in costing more money and time.
 
How do we install the required packages in the EFS file system?
To access the EFS file system, we need to create a new EC2 instance in AWS (Note: The EFS, lambda function and EC2 should be in the same Security Group and VPN). After creating an EC2 Instance, we need to mount the file system to the EC2 Instance. Now we can download the necessary pip packages into the EC2 Instance. [*How to install library on EFS & import in lambda* - Youtube](https://www.youtube.com/watch?v=FA153BGOV_A&ab_channel=SrceCde)
	
	
