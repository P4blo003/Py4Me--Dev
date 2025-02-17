# ---- MODULES ----
import json
# ---- VARIABLES ----

# ---- FUNCTIONS ----
def LoadFromJSON(filePath:str):
    """
    Try load a data from a given JSON file.
    """
    with open(filePath, 'r') as file:  
        data = json.load(file)
    return data