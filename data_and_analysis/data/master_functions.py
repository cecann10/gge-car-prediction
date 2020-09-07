#!/usr/bin/env python
# coding: utf-8

# In[6]:


import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[48]:


def make_model_df(make, url):
    '''
    Will return data for all cars listed on
    any result page of using the 'browse by model' tool on 
    https://www.fueleconomy.gov/feg/findacar.shtml.
    Tool forces narrowed search by make and model,
    so each result page scraped will be for a single
    make and model.  
    
    Inputs:
     - make = string of make of car's name
     - url = url for scraping from results of from
             https://www.fueleconomy.gov/feg/findacar.shtml
    
    Output:
    Dataframe for a single make & model of a car's:
    - Year
    - Model
    - Engine Capacity
    - Cylinders
    - Transmissions
    - Transmissions Speeds
    - Fuel Types
    - Greenhouse Gas Emissions
    - Miles-per-gallon

    '''
    results = requests.get(url)
    page = results.text

    soup = BeautifulSoup(page, "html5lib")

    #initiate data storage
    years = []                   #year of car
    models = []                  #model of car
    engine_capacities = []       #engine capacity volume in liters
    cylinders = []               #number of car's cylinders
    transmissions = []           #car's transmission type
    trans_speeds = []            #car's transmission speed
    fuel_types = []              #fuel type the car takes
    gg_emissions =[]             #greenhouse gas emissions from tailpipe of car in grams per mile
    mpgs = []                    #miles-per-gallon of car


    for element in soup.find_all('td', colspan="8"):

        #year
        for car_info in element.find_all('a'):
            year = car_info.text.split()[0]
            years.append(int(year))
        
        #model
        for car_info in element.find_all('a'):
            model = ' '.join(car_info.text.split()[2:])
            models.append(model)

        
        for car_details in element.find_all('span', class_="config"):
            
            # car combined volume capacity (vol_cap)
            engine_capacity = float(car_details.text.split(',')[0].strip(" L"))
            engine_capacities.append(engine_capacity)
            
            # cylinders
            cylinder = int(car_details.text.split(',')[1].strip(' cyl'))
            cylinders.append(cylinder)
            
            # transmission
            transmission = (car_details.text.split(',')[2]).split(' ')[1]
            transmissions.append(transmission)
            
            # transmission speed
            trans_speed = ((car_details.text.split(',')[2]).split(' ')[2].strip(')(-spd'))
            trans_speeds.append(trans_speed)

            # fuel types (e.g. premium gas, electric, regular gas)
            fuel_type = car_details.text.split(',')[-1]
            fuel_types.append(fuel_type)
    
    
    #greenhouse gas emissions (tailpipe)
    for gge_element in soup.find_all('div', class_="ghg-score"):
        gge = int(gge_element.text.strip(' grams/mile'))
        gg_emissions.append(gge)
            
    # CAR MPG
    for mpg_element in soup.find_all('td', class_="mpg-comb"):
        mpg = int(mpg_element.text)
        mpgs.append(mpg)


    #full dataframe        
    cars = pd.DataFrame({
    'year': years,
    'make': make,
    'model': models,
    'capacity_liters': engine_capacities,
    'cylinders': cylinders,
    'transmission': transmissions,
    'trans_speed': trans_speeds,
    'fuel_type': fuel_types,
    'gg_emissions': gg_emissions,
    'mpg': mpgs,
    })
    
    return cars


# In[20]:


def get_car_urls(make, models_list):
    '''
    Inputs: ([make], [list of models for make of car])
    Output: List of urls for all models under make inputted.
    '''
    url = "https://www.fueleconomy.gov/feg/PowerSearch.do?action=noform&path=1&year1=1984&year2=2021&make={}&baseModel={}&srchtyp=ymm"
    urls = []
    for model in models_list:
        file_url = url.format(make, model)
        urls.append(file_url)
    return urls

