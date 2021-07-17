"""Schema loading- and processing-related functions."""
from copy import deepcopy
from pathlib import Path
from warnings import warn

import yaml


def _get_entry_name(path):
    if path.suffix == ".yaml":
        return path.name[:-5]  # no .yaml
    else:
        return path.name


def load_schema(schema_path):
    """Load the schema into a dictionary.

    This function allows the schema, like BIDS itself, to be specified in
    a hierarchy of directories and files.
    File names (minus extensions) and directory names become keys
    in the associative array (dict) of entries composed from content
    of files and entire directories.

    Parameters
    ----------
    schema_path : str
        Folder containing yaml files or yaml file.

    Returns
    -------
    dict
        Schema in dictionary form.
    """
    schema_path = Path(schema_path)
    if schema_path.is_file() and (schema_path.suffix == ".yaml"):
        with open(schema_path) as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
    elif schema_path.is_dir():
        # iterate through files and subdirectories
        res = {
            _get_entry_name(path): load_schema(path)
            for path in sorted(schema_path.iterdir())
        }
        return {k: v for k, v in res.items() if v is not None}
    else:
        warn(f"{schema_path} is somehow nothing we can load")


def filter_schema(schema, **kwargs):
    """Filter the schema based on a set of keyword arguments.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.
    kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    new_schema : dict
        The filtered version of the schema.

    Notes
    -----
    This function calls itself recursively, in order to apply filters at
    arbitrary depth.

    Warning
    -------
    This function employs a *very* simple filter. It is very limited.
    """
    new_schema = deepcopy(schema)
    if isinstance(new_schema, dict):
        # Reduce values in dict to only requested
        for k, v in kwargs.items():
            if k in new_schema.keys():
                filtered_item = deepcopy(new_schema[k])
                if isinstance(filtered_item, dict):
                    filtered_item = {
                        k1: v1 for k1, v1 in filtered_item.items() if k1 in v
                    }
                else:
                    filtered_item = [i for i in filtered_item if i in v]
                new_schema[k] = filtered_item

            for k2, v2 in new_schema.items():
                new_schema[k2] = filter_schema(new_schema[k2], **kwargs)

    elif isinstance(new_schema, list):
        for i, item in enumerate(new_schema):
            if isinstance(item, dict):
                new_schema[i] = filter_schema(item, **kwargs)
    return new_schema
