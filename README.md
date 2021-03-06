## Predicting the Opening price of Nifty 50.

### Contents:

[Introduction](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#introduction)

[Data Source:](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#data-source)

- [More on the Datasets](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#more-on-the-datasets)

[Assumption of the Model](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#assumption-of-the-model)

[Procedure](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#procedure)

- [Getting and Cleaning the Data](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#1-getting-and-cleaning-the-data)

- [Pre-Processing the Data](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#2-pre-processing-the-data)

- [Exploratory Analysis](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#3-exploratory-analysis)

- [Fitting the Models](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#4-fitting-the-models)

- [Deploying the Model in AWS Lambda](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#5-deploying-the-model-in-aws-lambda)

[Drawbacks of the model](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#some-drawbacks-of-the-model)

[Diagonsis for the Drawbacks](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50#how-could-we-negate-these-drawbacks)

<p>&nbsp;</p>

### Introduction

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  The Goal of the project is to predict the opening level of the NIFTY 50 based on the sentiment of the news collected after the close of the market till the opening of the market on the next day. In addition to the news sentiment, we would be using other Indices to help us with the prediction.



#### Data Source: 

[News Headline Data](https://pulse.zerodha.com/pulse-news-dump.zip) 

The required Index price is pulled from [`yfinance library`](https://pypi.org/project/yfinance/).


<p>&nbsp;</p>
	
##### More on the Datasets:
	
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The NewsHeadlines data contains the news headlines from [Pulse](https://pulse.zerodha.com/), a financial news aggregator from [Zerodha](https://zerodha.com/).  The News Headlines Dataset contains the headlines, links and the date and time when it was published. The News headline timeline starts from 2014 and goes on till 2017. but also contain outlier dates, especially from the year 1970. Now coming to stock prices, we would be using `yfinance` module for pulling stock prices. `yfinance` is an API wrapper of yahoo finance, which can be used to pull the necessary data. Since the News data stretches from 2014 to 2017, we'd keep the years 2014 to 2017. 

So, which stock Index are interest in?
1. Nifty 50 (Obsiously):
	Nifty 50 is the benchmark Index used to gauge the National Stock Exchange (NSE). The index consist of 50 Indian listed stocks accounting to 13 important sectors in the National Stock Exchange.  

2. S&P 500 Index:
	S&P 500 is the benchmark Index used to gauge the major US stock exchanges (NASDAQ and NYSE). The Index doesn't have a strict criteria and any inclusion is based on the selection by a committe  S&P Dow Jones Indices. Th committe would assesses the company's merit using eight important critiera i.e Market Capitalzation, Public Float, role of the industry in the economy of the US, Financial Strength, Duration of time in the public market, domicile, liquidity and stock exchange. The Index contains 500 companies. 
	
3. Nikkie 225 Index:
	Nikkie 225 is the Stock index of the Toyko Stock Exchange. The index measures the performance of the top 225 publically traded in the Japanese top stock exchange. 


### Assumption of the Model:

1. The news headline would resemble that of a social media post.
2. The Opening Price of the NIFTY50 Index is highly influenced by the sentiment of the News flow. 
3. The time of the news would also influence the news.
4. The US & Japan markets influence the open price of the NIFTY index price.

### Procedure:

1) Getting and Cleaning the Data.
2) Pre-Processing the Data
3) Exploratory Analysis.
4) Fitting the Models.
5) Deploying the Model in AWS Lambda. 

#### 1. Getting and Cleaning the Data.

As with any data dataset, finding a raw data ready for analysis is never the case. And our datsets are no expection! So, we would start with News Headlines dataset. The required news headlines data is download from the above website and loaded for cleaning. The News data consisted of fewer data misplacement. Very few of 'Date_Time' consisted of the links or the News headlines. Cleaning of the same is done in the [Preprocessing_Newsheadline_data.py](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/Preprocessing_Newsheadline_data.py) script. 

As mentioned earlier for stock prices, we would be using `yfinance` to load all the required stock prices. So what are the data that interest us?
Before we look into the required data, let's talk about what we would require to build the model. It would be needing the move the US market, the Japanese market and the Indian Market.

So, the data we use for our analysis. 

1.  Closing prices of S&P 500.
2.  Open & Close of Nikkie 225.
3.  Open & Close of NIFTY 50.

#### 2. Pre-Processing the Data


The Headline is passed through the function `analzyer_polarity_score()` from vaderSentiment moudulues. <put what does it does here> The function would return the score  in the three columns, i.e. compound, neu(neutral), pos (positive) and neg (negative). 

[More about vaderSentiment](https://github.com/cjhutto/vaderSentiment)


With the sentiment scores figured out, we would now move to add weights to the score. Now why would be interested in adding? And how would we be assigning weights for the same?

Let us start with the latter question, the weights were assigned based on the published time of the particular news headline. Now coming back on the why we are doing so?
	
The rationale behind assigning weights to News or a piece of new information is an assumption that any News published way before the market opens would be scrutinized and analyzed in a manner that the panic initially created by the News would subside. Thereby nullifying the absolute effect on the market open. Hence to capture such actions, it would be beneficial to use weights.  


The data provided by the yfinace has no issues. Therefore we could safely assume that the data provided is accurate. But we shall be removing some columns, which render useless to our analysis. After removing the unnecessary, we could proceed to process our data as per the model requirement.

#### Why are we using the S&P500 & Nikkie Index??
The US markets usually decides the tempo for the rest of the financial markets around the globe, which was solidified by the high correlation between the S&P500 and the Nifty50. 
And coming to the Nikkie 225, the Japanese market also influences the Indian market. (due to a presence of co-integration and co-movement) [TESTING FINANCIAL INTEGRATION BETWEEN STOCK MARKET OF INDIA AND JAPAN: AN EMPIRICAL STUDY](https://www.srcc.edu/system/files/TESTING.pdf)

- `USMove`: Stores the S&P500 closing price difference.

- `JapanGap`: Stores the difference between the previous day closing price and the current days Opening prices. 

- `IndiaGap`: Stores the difference between the previous day closing price and the current days Opening price.

#### 3) Exploratory Analysis.

	
![newsheadlinescount](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index1.png)	
	
The NewsHeadlines dataset seems to have a substantial amount of news headlines after 2014. Hence we would base our study based on those days. 

Now let's have a look at how the sentiment of the newsheadlines dataset looks like, 

![hisOfUnwieghtedSentiplot](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index2.png)

What happens when we add up weights to the sentimental scores.

![hisOfwieghtedSentiplot](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index3.png)

We wil be summing all those up sentmental score for each day. 
![summedWights](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index5.png)

After summing up, the data seems to be normally distributed. Hence we would not be doing any transformation further on. 	

Let's move on to Stock prices. 
	
	
![closingPrice](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index4.png)

![stockHist](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index7.png)

![Statisonaryplot](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index6.png)
	
Before we use the stock data, we would be removing the outlier values, the ~ -5% fall of NIFTY Index would be dropped. 

![relationshipMeanPlot](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index8.png)

Let's have a look at the target varibale.

![Target](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/targetIndex.png)

Since there's an imbalance in our target varibale we would be oversampling the minority class.

#### 4) Fitting the Models.	
	
Let???s look at corrplot to see if we have any issues with multicollinearity (Assuming $~R^2 > 0.8$). 

![Corrplot](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index10.png)

There???s no high multicollinearity between the features. Hence we would not be dropping any features here.

![pairPlotOS](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index11.png)

![featureImp](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index12.png)

Since the Weekdays has very less influence on the target variable we would be dropping those features. 

![pairPlotOSFImp](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/index9.png)

The relations between the variables seems to be complex rather than being a simple linear model. Hence we would start our model by using complex models. 

The models to be employed

1. K Nearest Neighour
2. Decision Tree
3. Random Forest
4. XGBoost
5. Neural Networks

#### Results of the models:
	
##### 1. K Nearest Neighour
	

![cmknn](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/cmknnHy.png)
	
![crknn](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/crknnHy.png)


##### 2. Decision Tree
![cmDT](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/cmDTHy.png)

![crDT](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/crDTHy.png)
	
##### 3. Random Forest
	
![cmRF](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/cmRFHy.png)
	
![crRF](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/crRFHy.png)

##### 4. XGBoost

![cmXGB](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/cmxgbHy.png)

![crXGB](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/crxgbHy.png)

##### 5. Neural Networks

![cmNN](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/imgs/nncm.png)

##### Final results:
	
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>KNN</th>
      <th>DT</th>
      <th>RF</th>
      <th>XGB</th>
      <th>NN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Accuracy</th>
      <td>0.717</td>
      <td>0.596</td>
      <td>0.708</td>
      <td>0.696</td>
      <td>0.641</td>
    </tr>
    <tr>
      <th>F1_Score</th>
      <td>0.714</td>
      <td>0.600</td>
      <td>0.706</td>
      <td>0.697</td>
      <td>0.642</td>
    </tr>
    <tr>
      <th>AUC_Score</th>
      <td>0.788</td>
      <td>0.679</td>
      <td>0.855</td>
      <td>0.838</td>
      <td>0.807</td>
    </tr>
  </tbody>
</table>
	
By comparing all the above models, we would pick the Random Forest model, Since there is no significant improvement in the more complex models. 

[More on Modelling](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/PredictingOpeningPriceUsingNewsSentimentAndOtherIndex.ipynb)

#### 5) Deploying the Model in AWS Lambda. 
	
So we have fitted and choosen a model. Hence we move to deploying the model. We could connect the model with the Broker API, make a trading bot and live test the performance. But since the broker APIs are kind of expensive. We would deploy model in the cloud and live test the performance. To accomplish the same, We would need a program that would extract the required finance data from Yahoo Finance and the News data from the News API. The data would pass through the model, and the output from the model would store the result in the .csv file. 

How can we come about doing the same?
- We can set up a cronjob in our local machine.
- We can schedule a Github Workflow Action. 
- We can use a Cloud Service.

I???ll be choosing the cloud service (AWS) over the other choices because I would like to familiarize myself with Cloud Computing. 	
	
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
To access the EFS file system, we need to create a new EC2 instance in AWS (Note: The EFS, lambda function and EC2 should be in the same Security Group and VPN). After creating an EC2 Instance, we need to mount the file system to the EC2 Instance. Now we can download the necessary pip packages into the EC2 Instance. 

##### *Check out these tutorial to overcome both Network and Importing external packages issue*

[*How to install library on EFS & import in lambda* - Youtube](https://www.youtube.com/watch?v=FA153BGOV_A&ab_channel=SrceCde)
	

[How do I give internet access to a Lambda function that's connected to an Amazon VPC? -AWS Support](https://aws.amazon.com/premiumsupport/knowledge-center/internet-access-lambda-function/)
	
The code for deployment is [here](https://github.com/SanjayShetty01/PredictingOpeningPriceNifty50/blob/main/lambdafunction.py)	
### Some Drawbacks of the model:
	
1. The vaderSentiment module is mainly used to compute and assign the sentiment score for the social media sites like Twitter. Even though a news headline would mimic a tweet, the context of some financial move would not be captured by the vaderSentiment analyser.

For eg.
	
```python
analyzer.polarity_scores('HDFC delivers a bad quater')

```
{'compound': -0.5423, 'neg': 0.467, 'neu': 0.533, 'pos': 0.0}

```python
analyzer.polarity_scores('BoB delivers a bad quater')
```
{'compound': -0.5423, 'neg': 0.467, 'neu': 0.533, 'pos': 0.0}

Even though the HDFC result would affect the movement of NIFTY more than BoB. The sentimental score would be the same.

2. Using news sentimental value to predict the stock price would be considered to be a rookie mistake, especially if we would use options to trade with the predictions. We would be better off predicting the volatility instead of the price. This could also be considered an inherent issue with our model. 

	
### How could we negate these drawbacks?
1. As far as Volatity is considerd, we could get premium data provider to extract INDIA VIX data.  
 
2. To deal with the discrepancy in the vaderSentiment module. We could build an algorithm to deal with financial news data using a larger stock index price, preferably 5 min data.
	

