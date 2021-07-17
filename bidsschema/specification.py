"""Functions for interacting with the specification."""
import os.path as op


def download_schema(version="latest", out_dir="auto"):
    assert version == "latest", "No other versions supported yet."
    URL = "https://github.com/bids-standard/bids-specification"
    if version == "latest":
        URL = op.join(URL, "tree/master/src/schema")
