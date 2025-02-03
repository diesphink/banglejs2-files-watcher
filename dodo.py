#!/usr/bin/env python3

from upload import main
import asyncio
import logging
import requests

import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="dodo.log",
)

logger = logging.root


def download_weather_data():
    # Versão bash+jq do mesmo processo:
    # 'curl "wttr.in/sorocaba?format=j1" | jq "[.weather[] | {hourly:[.hourly[] | {tempC: .tempC|tonumber, chanceofrain: .chanceofrain|tonumber, weatherDesc: .weatherDesc[0].value, weatherCode: .weatherCode | tonumber}], date, mintempC: .mintempC | tonumber, maxtempC: .maxtempC|tonumber, avgtempC: .avgtempC | tonumber}]" > weather.json',

    logging.info("Downloading weather data")

    url = "https://wttr.in/sorocaba"
    params = {"format": "j1"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    weather = []

    weather = [
        {
            "hourly": [
                {
                    "tempC": int(hour["tempC"]),
                    "chanceofrain": int(hour["chanceofrain"]),
                    "weatherDesc": hour["weatherDesc"][0]["value"],
                    "weatherCode": int(hour["weatherCode"]),
                }
                for hour in day["hourly"]
            ],
            "date": day["date"],
            "mintempC": int(day["mintempC"]),
            "maxtempC": int(day["maxtempC"]),
            "avgtempC": int(day["avgtempC"]),
        }
        for day in data["weather"]
    ]

    with open("weather.json", "w") as f:
        json.dump(weather, f)


def task_download_data():
    return {
        "actions": [
            # 'curl "wttr.in/sorocaba?format=j1" | jq "[.weather[] | {hourly:[.hourly[] | {tempC: .tempC|tonumber, chanceofrain: .chanceofrain|tonumber, weatherDesc: .weatherDesc[0].value, weatherCode: .weatherCode | tonumber}], date, mintempC: .mintempC | tonumber, maxtempC: .maxtempC|tonumber, avgtempC: .avgtempC | tonumber}]" > weather.json',
            download_weather_data,
        ],
        "targets": ["weather.json"],
    }


def run_sync():
    logging.info("Syncing data")
    asyncio.run(main("f2:dc:a8:e1:41:35", ["weather.json"], 0, 20, "sphclock.app.js"))


def task_sync():
    return {
        "actions": [run_sync],
        "file_dep": ["weather.json"],
    }
