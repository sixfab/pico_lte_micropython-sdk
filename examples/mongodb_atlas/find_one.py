from pico_lte.core import PicoLTE
from pico_lte.common import debug

debug.set_level(0)

picoLTE = PicoLTE()

payload = {
    "dataSource": "PicoLTE",
    "database": "sample_guides",
    "collection": "planets",
    "filter": {"_id": {"$oid": "621ff30d2a3e781873fcb660"}},
}

debug.info("Network Registration...")
result = picoLTE.mongodb_atlas.find_one(payload)
debug.info("Result:", result)
