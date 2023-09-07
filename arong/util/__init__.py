import json
import os

def mkdirs(file):
    parent_dir = os.path.dirname(file)
    os.makedirs(parent_dir, exist_ok=True)
    
def pprint(d):
    """
    Pretty print
    """
    print(pprints(d))


def pprints(d):
    """
    Pretty print string
    """
    return json.dumps(d, indent="\t")