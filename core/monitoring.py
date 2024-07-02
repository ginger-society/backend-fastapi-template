from typing import Callable
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Counter

COUNT_METRIC = Counter(
    "http_requested_languages_total_with_join",
    "Number of times a certain language has been requested.",
    labelnames=("langs",),
)


# this can intercept request add metrics
def http_requested_languages_total() -> Callable[[Info], None]:
    def instrumentation(info: Info) -> None:
        # info.request
        print("running prom middleware -----------)))))")

    return instrumentation
