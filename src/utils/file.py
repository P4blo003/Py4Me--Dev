# ---- MODULES ----
import json
# ----

# ---- FUNCTIONS ----
def getDataFromJSON(filePath:str):
    """
    Load the data from a given file path.

    :param str filePath:
        File's path.
    """
    try:

        with open(filePath,'r') as file:    # Open the file in read mode.
            data = json.load(file)          # Load the data from the file.

    except Exception as ex:                 # If something is bad.
        pass

    return data
# ----