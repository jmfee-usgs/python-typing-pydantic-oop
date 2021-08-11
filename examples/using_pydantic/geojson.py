from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from typing_extensions import Literal
import pydantic


class Geometry(pydantic.BaseModel):
    type: str
    coordinates: Sequence


class Feature(pydantic.BaseModel):
    type: Literal["Feature"]
    id: str
    properties: Union[Dict[str, Any], pydantic.BaseModel]
    geometry: Optional[Geometry]

    class Config:
        extra = "allow"


class FeatureCollection(pydantic.BaseModel):
    type: Literal["FeatureCollection"]
    features: Sequence[Feature]
    bbox: Optional[List[float]]

    class Config:
        extra = "allow"


class PointGeometry(Geometry):
    type: Literal["Point"]
    coordinates: Sequence[float]

    @property
    def depth(self) -> Optional[float]:
        if len(self.coordinates) > 2:
            return self.coordinates[2]
        return None

    @property
    def latitude(self) -> float:
        return self.coordinates[1]

    @property
    def longitude(self) -> float:
        return self.coordinates[0]
