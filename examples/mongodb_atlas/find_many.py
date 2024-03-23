"""
Example code for finding documents in MongoDB Atlas with using its Data API.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
  "mongodb_atlas": {
    "base_url": [DATA_API_BASE_URL],
    "api_key": [YOUR_API_KEY]
  }
}
"""

import json

from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload = {
    "dataSource": "PicoLTE",
    "database": "sample_mflix",
    "collection": "comments",
    "filter": {"movie_id": {"$oid": "573a1391f29313caabcd7a34"}},
    "projection": {"movie_id": 1, "text": 1},
}

payload = json.dumps(payload)

debug.info("Network Registration...")
result = picoLTE.mongodb_atlas.find_many(payload)
debug.info("Result:", result)
