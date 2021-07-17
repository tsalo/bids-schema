import importlib.util
import json
import os.path as op

spec = importlib.util.spec_from_file_location(
    "_version", op.join(op.dirname(__file__), "bidsschema/_version.py")
)
_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_version)

VERSION = _version.get_versions()["version"]
del _version

# Get list of authors from Zenodo file
with open(op.join(op.dirname(__file__), ".zenodo.json"), "r") as fo:
    zenodo_info = json.load(fo)
authors = [author["name"] for author in zenodo_info["creators"]]
authors = [author.split(", ")[1] + " " + author.split(", ")[0] for author in authors]

AUTHOR = "bidsschema developers"
COPYRIGHT = "Copyright 2021--, bidsschema developers"
CREDITS = authors
LICENSE = "MIT"
MAINTAINER = "Taylor Salo"
EMAIL = "tsalo006@fiu.edu"
STATUS = "Prototype"
URL = "https://github.com/bids-specification/bids-schema"
PACKAGENAME = "bidsschema"
DESCRIPTION = ""
LONGDESC = ""

DOWNLOAD_URL = "https://github.com/bids-specification/{name}/archive/{ver}.tar.gz".format(
    name=PACKAGENAME, ver=VERSION
)

REQUIRES = [
    "numpy"
]

TESTS_REQUIRES = [
    "codecov",
    "coverage",
    "coveralls",
    "flake8-black",
    "flake8-docstrings",
    "flake8-isort",
    "pytest",
    "pytest-cov",
]

EXTRA_REQUIRES = {
    "doc": [
    ],
    "tests": TESTS_REQUIRES,
}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES["all"] = list(set([v for deps in EXTRA_REQUIRES.values() for v in deps]))

# Package classifiers
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering",
]
