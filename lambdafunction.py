from io import StringIO
import sys



def lambda_handler(event, context):

  sys.path.append("/mnt/packages")

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
  import pytz
  from lxml import html
  import requests
  import time
# Load all the necessary stock datas

# Getting the Nifty50 price data from the website
  IST = pytz.timezone('Asia/Kolkata')

# Load all the necessary stock datas

# Getting the Nifty50 price data from the website

  urlNifty = "https://finance.yahoo.com/quote/%5ENSEI" 
 
  PrevClose = 0
 
  while PrevClose == 0:
    try:
      response = requests.get(
      urlNifty, 
      headers={
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})

      parser = html.fromstring(response.text)
  
      PrevClose = parser.xpath(
      '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]//text()')

      Open = parser.xpath(
      '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[1]/table/tbody/tr[2]/td[2]//text()')
    
    except:
      time.sleep(10)
      continue
    
    
  INDPrevClose = PrevClose[0].replace(',', '')

  INDPrevClose = float(INDPrevClose)

  INDOpen = Open[0].replace(',', '')
  INDOpen = float(INDOpen)


  IndiaGap = round((INDOpen - INDPrevClose)/INDPrevClose*100,2)

# Getting the US Market price data from the website

  SNPurl = 'https://finance.yahoo.com/quote/%5EGSPC'
  
  
  PrevClose = 0
  
  while PrevClose == 0:
    try:
      
      response = requests.get(
      SNPurl, 
      headers={
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})

      parser = html.fromstring(response.text)

      PrevClose = parser.xpath(
      '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[3]/div[1]/div/fin-streamer[3]/span//text()')
      
    except:
      time.sleep(10)
      continue

  PrevClose = PrevClose[0].replace('%', '').replace('(', '').replace(')','')

  USMove = float(PrevClose)


# Getting the Nikkei Market price data from the website     

  JapURL = 'https://finance.yahoo.com/quote/%5EN225'
  
  PrevClose = 0
  
  while PrevClose == 0:
    
    try:
      response = requests.get(
      JapURL, 
      headers={
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"})

      parser = html.fromstring(response.text)

      PrevClose = parser.xpath(
      '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]//text()')

      Open = parser.xpath(
      '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[1]/table/tbody/tr[2]/td[2]//text()')

    except:
      time.sleep(10)
      continue
    
    
    
  JapPrevClose = PrevClose[0].replace(',', '')

  JapPrevClose = float(JapPrevClose)

  JapOpen = Open[0].replace(',', '')

  JapOpen = float(JapOpen)

  JapGap = round((JapOpen - JapPrevClose)/JapPrevClose*100,2)



# Getting News Data using the API

  api = NewsApiClient(api_key='xxxxxxxxxxxxxxxxxxxxxxxx')

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
    aws_access_key_id = 'xxxxxxxxxxxxxxxxxxxxx',
    aws_secret_access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx',
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
      aws_secret_access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
      region_name = 'us-east-1'
)
 

  obj = client.get_object(
      Bucket = 'myniftyperformance',
      Key = 'theperformancedata.csv'
)

  data = pd.read_csv(obj['Body'])

  updatedFile = pd.concat([data,finalData])


  csv_buf = StringIO()
  updatedFile.to_csv(csv_buf, header=True, index=False)
  csv_buf.seek(0)
  client.put_object(Bucket='myniftyperformance', Body=csv_buf.getvalue(), Key='theperformancedata.csv')
  
  print('Success')
