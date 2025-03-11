import requests
import logging
from datetime import datetime, timedelta
from .Exceptions import InvalidFinalDate, InvalidInitialDate
from dotenv import load_dotenv
import os

logging.basicConfig(
    filename='app.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PySimFin:
  def __init__(self):
    self.__api_key='1c8ac883-1180-4ed0-93cc-cfff0a297631'
    self.__headers = {'accept':'application/json','Authorization': f'{self.__api_key}'}
    logging.info('API Key and authenticator set up correctly.')
  def get_share_prices(self,ticker:str,start:str,end:str):
    logging.info('Checking the initial and final dates to prevent errors in the web.')
    if start>end or start<'2018-03-05':
      raise InvalidInitialDate('Cannot input initial date greater than final date nor before 2018-03-05')
    elif end<start or end>'2025-03-04':
      raise InvalidFinalDate('Cannot input final date lower than initial date nor after 2025-03-04')
    else:
      new_start=str(datetime.strptime(start,'%Y-%m-%d').date()-timedelta(days=5))
      logging.info('Correct input dates, getting the response from the web.')
      self.__url=f'https://backend.simfin.com/api/v3/companies/prices/verbose?ticker={ticker}&start={new_start}&end={end}'
      response=requests.get(self.__url,headers=self.__headers)
      if response.status_code == 200:
        data = response.json()
        data_list=[]
        if data!=[]:
          for i in data[0]['data']:
            data_list.append(i['Last Closing Price'])
          last_list=data_list[-3:]
          return f'The closing prices for the given dates are: {last_list}'#\nThe predicted closing price for the next day is:{next_day_price:.2f}.'
        else:
          return f'No data available between {start} and {end}.'
      else:
        logging.error(f'Unable to retrieve data, error:{response.status_code}. Please check the definition of these mistakes to correct your input data:\n400 - Bad request\n404 - API not found\n429 - Rate limits exceeded, see section Rate Limits.')
  
  
  #def get_financial_statement(self,ticker:str,start:str,end:str):
    #self.url=f'https://backend.simfin.com/api/v3/companies/financials/statements/compact?id=&ticker={self.ticker}&start={self.start}&end={self.end}'
    #headers = {'Authorization': f'Bearer {self.api_key}'}
    #response=requests.get(self.url,headers=headers)