from datetime import datetime
from typing import Dict, List, Optional, Sequence, Set, Union

from pydantic import BaseModel, Field, validator
import requests
from typing_extensions import Literal

from ..time import parse_milliseconds
from .geojson import Feature, FeatureCollection, PointGeometry


class EarthquakeFeatureProperties(BaseModel):
    alert: Optional[Literal["green", "yellow", "orange", "red"]]
    cdi: Optional[float]
    code: str
    detail: str
    dmin: Optional[float]
    felt: Optional[int]
    gap: Optional[float]
    ids: Set[str]
    mag: Optional[float]
    magType: Optional[str]
    mmi: Optional[float]
    net: str
    nst: Optional[int]
    place: str
    rms: Optional[float]
    sig: int
    sources: Set[str] = Field(default_factory=set)
    status: Literal["automatic", "deleted", "reviewed"]
    time: datetime
    title: str
    tsunami: Optional[int]
    type: str = "earthquake"
    types: Set[str] = Field(default_factory=set)
    tz: Optional[float]
    updated: datetime
    url: str

    # feeds use millisecond timestamps, pydantic autodetect fails near epoch
    _parse_time = validator("time", allow_reuse=True, pre=True)(parse_milliseconds)
    _parse_updated = validator("updated", allow_reuse=True, pre=True)(
        parse_milliseconds
    )

    @validator("ids", pre=True)
    def _parse_ids(cls, ids: Optional[str]) -> Set[str]:
        values = (ids or "").split(",")
        return set([id for id in values if id])

    @validator("sources", pre=True)
    def _parse_sources(cls, sources: Optional[str]) -> Set[str]:
        values = (sources or "").split(",")
        return set([s for s in values if s])

    @validator("types", pre=True)
    def _parse_types(cls, types: Optional[str]) -> Set[str]:
        values = (types or "").split(",")
        return set([t for t in values if t])


class EarthquakeFeature(Feature):
    # override with more specific types
    properties: EarthquakeFeatureProperties
    geometry: Optional[PointGeometry]

    def has_product_type(self, product_type: str) -> bool:
        return product_type in self.properties.types


# summary queries/feeds include detail link in properties


class EarthquakeSummaryFeatureProperties(EarthquakeFeatureProperties):
    detail: str


class EarthquakeSummaryFeature(EarthquakeFeature):
    properties: EarthquakeSummaryFeatureProperties

    def load_detail(self) -> "EarthquakeDetailFeature":
        response = requests.get(self.properties.detail)
        response.raise_for_status()
        return EarthquakeDetailFeature(**response.json())


class EarthquakeCatalog(FeatureCollection):
    # override with specific feature type
    features: Sequence[EarthquakeSummaryFeature]


# detail feed includes products


class Content(BaseModel):
    contentType: str
    lastModified: datetime
    length: int
    sha256: Optional[str]

    # feeds use millisecond timestamps, pydantic autodetect fails near epoch
    _parse_lastModified = validator("lastModified", allow_reuse=True, pre=True)(
        parse_milliseconds
    )


class ByteContent(Content):
    bytes: str


class UrlContent(Content):
    url: str


class Product(BaseModel):
    indexid: Optional[str]
    indexTime: datetime
    id: str
    type: str
    code: str
    source: str
    updateTime: datetime
    status: str = "UPDATE"
    properties: Dict[str, str]
    preferredWeight: Optional[int]
    contents: Dict[str, Union[ByteContent, UrlContent]]

    # feeds use millisecond timestamps, pydantic autodetect fails near epoch
    _parse_indexTime = validator("indexTime", allow_reuse=True, pre=True)(
        parse_milliseconds
    )
    _parse_updateTime = validator("updateTime", allow_reuse=True, pre=True)(
        parse_milliseconds
    )


class EarthquakeDetailFeatureProperties(EarthquakeFeatureProperties):
    products: Dict[str, List[Product]]


class EarthquakeDetailFeature(EarthquakeFeature):
    properties: EarthquakeDetailFeatureProperties
