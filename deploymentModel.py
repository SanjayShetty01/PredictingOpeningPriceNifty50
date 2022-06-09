# import the library

import numpy as np
import yfinance as yf
import pandas as pd
from newsapi.newsapi_client import NewsApiClient
import datetime as dt
from datetime import date , timedelta, datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pickle
import boto3
import sklearn


# Load all the necessary stock datas

# Getting the Nifty50 price data from the website
NIFTYticker = '^NSEI'

NIFTYData = yf.Ticker(NIFTYticker)
todayNifty = NIFTYData.history(period='2d')

prevClosePrice = todayNifty['Close'][0]

todayOpenPrice = todayNifty['Open'][1]

IndiaGap = round((todayOpenPrice - prevClosePrice)/prevClosePrice*100,2)

# Getting the US Market price data from the website

SP = '^GSPC'

SPData = yf.Ticker(SP)
todaySP = SPData.history(period='2d')

USMove= round((todaySP['Close'].pct_change())*100,2)[1]


# Getting the Nikkei Market price data from the website     

Japanticker = '^N225'

NikkeiData = yf.Ticker(Japanticker)
todayNikkei = NikkeiData.history(period='2d')

JapanClosePrice = todayNikkei['Close'][0]
JapanOpenPrice = todayNikkei['Open'][1]

JapGap = round((JapanOpenPrice - JapanClosePrice)/JapanClosePrice*100,2)


# Getting News Data using the API

api = NewsApiClient(api_key='xxxxxxxxxxxxxxxxxxxxxxxxx')

today = date.strftime(date.today(), '%Y-%m-%d')
todayTime = 'T09:15:00'
today = today + todayTime

yesterday = date.strftime(date.today() - timedelta(1), '%Y-%m-%d')
yesterdayTime = 'T03:30:00'
yesterday = yesterday + yesterdayTime

news = api.get_everything( domains = 'moneycontrol.com',
                    language = 'en', 
                    to = today,
                    from_param=yesterday,
                    page = 1,page_size= 100)

news = news['articles']

NewsContent = []
NewsTime = []

for num in range(len(news)):
  NewsContent.append(news[num]['title'])
  NewsTime.append(news[num]['publishedAt'])


newsheadlines = pd.DataFrame(list(zip(NewsTime, NewsContent)), columns=['DateTime', 'Headlines'])

newsheadlines['DateTime'] = pd.to_datetime(newsheadlines.DateTime,format = '%Y-%m-%d %H:%M:%S.%f')

today = dt.datetime.strptime(today,'%Y-%m-%dT%H:%M:%S') 
yesterday = dt.datetime.strptime(yesterday,'%Y-%m-%dT%H:%M:%S') 

newsheadlines['DateTime'] = newsheadlines.DateTime.apply(lambda d: d.replace(tzinfo=None))

newsheadlines['DateTime'] = newsheadlines['DateTime'] + pd.Timedelta(hours=8, minutes = 30)

newsheadlines = newsheadlines[(newsheadlines.DateTime.dt.date == today.date())]

# using VADAR package to get a numerical value for each headlines

analyzer = SentimentIntensityAnalyzer()

newsheadlines['compound'] = [analyzer.polarity_scores(x)['compound'] for x in newsheadlines['Headlines']]
newsheadlines['negative_score'] = [analyzer.polarity_scores(x)['neg'] for x in newsheadlines['Headlines']]
newsheadlines['neutral_score'] = [analyzer.polarity_scores(x)['neu'] for x in newsheadlines['Headlines']]
newsheadlines['positive_score'] = [analyzer.polarity_scores(x)['pos'] for x in newsheadlines['Headlines']]

newsheadlines = newsheadlines.drop(columns='Headlines', axis = 1)

conditions = [
      ((newsheadlines.DateTime.dt.time > dt.time(0,0)) & (newsheadlines.DateTime.dt.time <= dt.time(3,00))),
      ((newsheadlines.DateTime.dt.time > dt.time(3,00)) & (newsheadlines.DateTime.dt.time <= dt.time(6,00))),
      ((newsheadlines.DateTime.dt.time > dt.time(6,00)) & (newsheadlines.DateTime.dt.time <= dt.time(9,00))),
      ((newsheadlines.DateTime.dt.time > dt.time(9,00)) & (newsheadlines.DateTime.dt.time <= dt.time(12,00))),
      ((newsheadlines.DateTime.dt.time > dt.time(12,00)) & (newsheadlines.DateTime.dt.time <= dt.time(15,00))),
      ((newsheadlines.DateTime.dt.time > dt.time(15,00)) & (newsheadlines.DateTime.dt.time <= dt.time(18,00)))            
]

values = [0.5, 0.6 , 0.7 ,0.8,0.9,1]

newsheadlines['Weight'] = np.select(conditions, values)

newsheadlines['WeightedScoreCompounded'] = round(newsheadlines['compound'] * newsheadlines['Weight'],2) 
newsheadlines['WeightedScoreNeutral'] = round(newsheadlines['neutral_score'] * newsheadlines['Weight'],2)
newsheadlines['WeightedScorePositive'] = round(newsheadlines['positive_score'] * newsheadlines['Weight'],2)
newsheadlines['WeightedScoreNegative'] = round(newsheadlines['negative_score'] * newsheadlines['Weight'],2)

newsheadlines = newsheadlines.groupby([newsheadlines['DateTime'].dt.date]).sum()

newsheadlines.reset_index(inplace = True)

newsheadlines.drop(columns = ['DateTime','compound', 'negative_score', 'neutral_score', 'positive_score', 'Weight'], inplace=True)

USMove = pd.Series(USMove)
JapGap = pd.Series(JapGap)

USMove = USMove.rename('USMove')
JapGap = JapGap.rename('JapGap')

marketData = JapGap.to_frame().join(USMove)

finalData = newsheadlines.join(marketData)


resource = boto3.resource('s3',
    aws_access_key_id = 'xxxxxxxxxxxxx',
    aws_secret_access_key = 'xxxxxxxxxxxxxxxx',
    region_name = 'us-east-1')
model = pickle.loads(resource.Bucket('myniftyperformance').Object('finalized_model.sav').get()['Body'].read())

prediction = model.predict(finalData)


if prediction[0] == 0:
  predictedStatus = 'flat'
  print('The Opening would be flat (i.e the Nifty 50 would be between -0.25 and 0.25)')

elif prediction[0] == 1:
  predictedStatus = 'negative'
  print('The Opening would be negative (i.e the Nifty 50 would be below -0.25)')

elif prediction[0] == 2:
  predictedStatus = 'positive'
  print('The Opening would be positive (i.e the Nifty 50 would be above 0.25)')


if IndiaGap :
  IndiaGapStatus = 'flat'

elif IndiaGap == 1:
  IndiaGapStatus = 'negative'

elif IndiaGap == 2:
  IndiaGapStatus = 'positive'


IndiaGapCondition = [
    ((-0.25 <= IndiaGap) & (IndiaGap <= 0.25)),
    ((0.25 < IndiaGap)),
    ((-0.25 > IndiaGap))
]

valueInd = ['flat','positive','negative']

IndiaGapStatus = np.select(IndiaGapCondition,valueInd )

IndiaGapStatus = pd.Series(IndiaGapStatus)
predictedStatus = pd.Series(predictedStatus)

IndiaGapStatus = IndiaGapStatus.rename('IndiaGapStatus')
predictedStatus = predictedStatus.rename('predictedStatus')

comparsion = IndiaGapStatus.to_frame().join(predictedStatus)

finalData = finalData.join(comparsion)

todayDate = today.date()

todayDate = pd.Series(todayDate)
todayDate = todayDate.rename('Date')

finalData = finalData.join(todayDate)

client = boto3.client(
    's3',
    aws_access_key_id = 'xxxxxxxxxxxxxxxxxxxxxx',
    aws_secret_access_key = 'xxxxxxxxxxxxxxxxxxxxxxx',
    region_name = 'us-east-1'
)
 

obj = client.get_object(
    Bucket = 'myniftyperformance',
    Key = 'theperformancedata.csv'
)

data = pd.read_csv(obj['Body'])

updatedFile = pd.concat([data,finalData])

obj.put_object(Bucket = 'myniftyperformance',Key = 'theperformancedata.csv',Body=updatedFile)



