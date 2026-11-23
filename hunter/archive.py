# This file is the only part of the project that talks to NASA.
# Keeping that in one place means that if NASA changes something,
# this is the one file I have to fix.
import httpx

# The address of NASA's query service.
NASA_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# The columns I want for each planet. These names come from NASA's
# column documentation.
# pl_name = planet name, hostname = the star it orbits,
# pl_rade = radius in Earth radii, pl_orbper = orbital period in days,
# pl_bmasse = mass in Earth masses, disc_year = year it was discovered,
# discoverymethod = how it was found.
COLUMNS = "pl_name, hostname, pl_rade, pl_orbper, pl_bmasse, disc_year, discoverymethod"


# "async def" means this function can wait for NASA without freezing the
# whole server. While we wait, the server can answer other visitors.
async def fetch_planets(limit: int = 20):
    # Build the question for NASA. "top" limits how many rows come back.
    query = f"select top {limit} {COLUMNS} from pscomppars"

    # These become the "?query=...&format=json" part of the address.
    params = {"query": query, "format": "json"}

    # Open a connection, and give up if NASA takes longer than 30 seconds.
    async with httpx.AsyncClient(timeout=30) as client:
        # "await" means: pause here until NASA replies, but let the
        # server do other work in the meantime.
        response = await client.get(NASA_URL, params=params)

        # If NASA replied with an error (like 500), raise an error here
        # instead of quietly carrying on with bad data.
        response.raise_for_status()

        # Turn NASA's JSON text into a Python list of dictionaries.
        return response.json()