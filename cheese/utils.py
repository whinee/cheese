from typing import Any, Dict

from settings import stg

YAHML = stg(None, "yamhl.yml")

def ddir(d: Dict[Any, Any], dir: str, de: Any={}) -> Any:
    """
    Retrieve dictionary value using recursive indexing with a string.
    ex.:
        `ddir({"data": {"attr": {"ch": 1}}}, "data/attr/ch")`
        will return `1`


    Args:
        dict (dict): Dictionary to retrieve the value from.
        dir (str): Directory of the value to be retrieved.

    Returns:
        op (Any): Retrieved value.
    """
    op = d
    for a in dir.split("/"):
        op = op.get(a)
        if not op:
            break
    return op or de