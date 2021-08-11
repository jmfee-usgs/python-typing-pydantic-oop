from dateutil.parser import isoparse

from .get_catalog import get_catalog


# get events using pydantic
catalog = get_catalog(
    starttime=isoparse("2021-01-01"),
    endtime=isoparse("2021-08-11"),
    producttype="finite-fault",
)
events = catalog.features
print(events[0])

# format list of events
print(f"{len(events)} matching events")
for event in events:
    props = event.properties
    time = props.time.date().isoformat()
    print(f"{time} - M{props.mag:.1f} {props.place}")
