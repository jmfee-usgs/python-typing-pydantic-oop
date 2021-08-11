from datetime import datetime
import logging
from typing import Dict

import requests


# default url for get events
DEFAULT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def get_catalog(
    starttime: datetime,
    endtime: datetime,
    url: str = DEFAULT_URL,
    **kwargs,
) -> Dict:
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
        other keyword arguments are passed as query parameters
        see https://earthquake.usgs.gov/fdsnws/event/1/

    Returns
    -------
    GeoJson Feature Collection as Dict.
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
    # response is json (a geojson featurecollection)
    catalog = response.json()
    return catalog
