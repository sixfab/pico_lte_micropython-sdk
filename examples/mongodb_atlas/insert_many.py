"""
Example code for inserting documents in MongoDB Atlas with using its Data API.

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
    "documents": [
        {
            "name": "Mercedes Tyler",
            "email": "mercedes_tyler@fakegmail.com",
            "movie_id": {"$oid": "5a9427648b0beebeb69579e7"},
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla in.",
        },
        {
            "name": "John Bishop",
            "email": "john_bishop@fakegmail.com",
            "movie_id": {"$oid": "573a1390f29313caabcd446f"},
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla in.",
        },
    ],
}

payload = json.dumps(payload)

debug.info("Network Registration...")
result = picoLTE.mongodb_atlas.insert_many(payload)
debug.info("Result:", result)
