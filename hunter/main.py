
# FastAPI is a tool that turns Pythin functions into web addresses
from fastapi import FastAPI, HTTPException, Query
import httpx

from hunter.archive import fetch_planets

# This creates the app.

app = FastAPI(title="Exoplanet Hunter")

# This is a decorator. Basically when someone visits the site
# the address "/" runs the functions right below.

@app.get("/")
def home():
    # Return a Python dictionary (a set of labels and values). FastAPI
    # automatically converts it to JSON, a text format that browsers and other
    # programs can read, and sends it back to whoever visited.
    return {"message": "Server up "}


# This endpoint returns a list of planets from NASA.
# "limit" comes from the address, like /planets?limit=5.
# Query(20, ge=1, le=100) means: default to 20, and refuse anything below 1
# or above 100. That protects NASA's server and keeps bad input out of
# the query we build.
@app.get("/planets")
async def list_planets(limit: int = Query(20, ge=1, le=100)):
    try:
        planets = await fetch_planets(limit)
    except httpx.HTTPError:
        # 502 means "I'm a middleman and the server behind me failed."
        raise HTTPException(status_code=502, detail="Could not get data from NASA right now.")

    return {"count": len(planets), "planets": planets}