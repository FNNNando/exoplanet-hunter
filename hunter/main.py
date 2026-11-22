
# FastAPI is a tool that turns Pythin functions into web addresses
from fastapi import FastAPI

# This creates the app.

app = FastAPI(title="Exoplanet Hunter")

# This is a decorator. Basically when someone visits the site
# the address "/" runs the functions right below.

@app.get("/")
def home():
    # We return a Python dictionary (a set of labels and values). FastAPI
    # automatically converts it to JSON, a text format that browsers and other
    # programs can read, and sends it back to whoever visited.
    return {"message": "Server up "}