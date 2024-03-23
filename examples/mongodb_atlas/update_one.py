"""
Example code for updating a document in MongoDB Atlas with using its Data API.

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
    "filter": {"_id": {"$oid": "5a9427648b0beebeb6957b28"}},
    "update": {
        "$set": {
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam vitae."
        }
    },
    "upsert": False,
}

payload = json.dumps(payload)

debug.info("Network Registration...")
result = picoLTE.mongodb_atlas.update_one(payload)
debug.info("Result:", result)
