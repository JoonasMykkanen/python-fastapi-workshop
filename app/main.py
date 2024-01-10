# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jmykkane <jmykkane@student.hive.fi>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/01/10 13:41:36 by jmykkane          #+#    #+#              #
#    Updated: 2024/01/10 14:37:32 by jmykkane         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Query
from pprint import pprint
from fastapi import Path
import pathlib
import json

class Coordinates(BaseModel):
    lat: float
    lon: float

class Location(BaseModel):
    city: str
    coordinates: Coordinates

class Restaurant(BaseModel):
    name: str
    id: str
    description: str
    location: Location

app = FastAPI(title='Restaurant API by jmykkane')

@app.get('/')
def hello_world():
    return 'Nothing to see here'

@app.get('/restaurants')
def get_restaurants() -> list[Restaurant]:
    file_path = pathlib.Path(__file__).parent / 'restaurants.json'
    with open(file_path) as file:
        data = json.load(file)

    if not data:
        return {'message': 'Error with database'}, 500

    restaurants = []
    for restaurant in data['restaurants']:
        name = restaurant['name']
        id  = restaurant['id']
        description = restaurant['description']
        lon, lat = restaurant['location']
        city = restaurant['city']
        
        restaurants.append(Restaurant(
            name=name,
            id=id,
            description=description,
            location=Location(city=city, coordinates=(Coordinates(lat=lat, lon=lon))),
        ))

    return restaurants

@app.get('/restaurants/{id}')
def get_one_restaurant(id):
    file_path = pathlib.Path(__file__).parent / 'restaurants.json'
    with open(file_path) as file:
        data = json.load(file)

    if not data:
        return {'message': 'Error with database'}, 500

    try:
        restaurants = []
        for restaurant in data['restaurants']:
            if restaurant['id'] == id:
                lon, lat = restaurant['location']
                response = Restaurant(
                    name=restaurant['name'],
                    id = restaurant['id'],
                    description = restaurant['description'],
                    location=Location(city=restaurant['city'], coordinates=Coordinates(lat=lat, lon=lon))
                )
                if response:
                    return response
                else:
                    return {'Message': 'not found'}, 404

    except Exception as e:
        print(f'Error at get:restaurants/id: {e}')
        return {'Message': f'internal server error: {e}'}, 500
    