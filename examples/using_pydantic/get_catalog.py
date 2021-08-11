from datetime import datetime
import logging

import requests

from .earthquake_catalog import EarthquakeCatalog, EarthquakeDetailFeature


# default url for get events
DEFAULT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def get_catalog(
    starttime: datetime,
    endtime: datetime,
    url: str = DEFAULT_URL,
    **kwargs,
) -> EarthquakeCatalog:
    """Load events from the USGS Earthquake Web Service.

    Arguments
    ---------
    starttime:
        minimum event time
    endtime:
        maximum event time
    url:
        url for FDSN Event web service query endpoint
    **kwargs
        other keyword arguments are passed as query parameters.
        see https://earthquake.usgs.gov/fdsnws/event/1/

    Returns
    -------
    List of matching event geojson features.
    """
    response = requests.get(
        url=url,
        params={
            "endtime": endtime.isoformat(),
            "format": "geojson",
            "starttime": starttime.isoformat(),
            **kwargs,
        },
    )
    logging.info(f"Loaded {response.url}")
    response.raise_for_status()
    # parse response (a geojson featurecollection)
    return EarthquakeCatalog(**response.json())


def get_event(id: str, url: str = DEFAULT_URL, **kwargs):
    response = requests.get(
        url=url,
        params={
            "eventid": id,
            "format": "geojson",
            **kwargs,
        },
    )
    logging.info(f"Loaded {response.url}")
    response.raise_for_status()
    return EarthquakeDetailFeature(**response.json())
