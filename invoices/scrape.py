import requests


name = "Test"
search_url = f"https://developers.kvk.nl/test/api/v1/zoeken?handelsnaam={name}&pagina=1&aantal=10"


def get_field(data, key):
    if key in data.keys():
        return data[key]
    return None

def get_address(kvk_id):
    url = f"https://developers.kvk.nl/test/api/v1/basisprofielen/{kvk_id}?geoData=false"
    r = requests.get(url)
    resp = r.json()
    if (
        "hoofdvestiging" in resp["_embedded"].keys()
        and "adressen" in resp["_embedded"]["hoofdvestiging"].keys()
        and len(resp["_embedded"]["hoofdvestiging"]["adressen"]) > 1
    ):
        address = resp["_embedded"]["hoofdvestiging"]["adressen"][0]
        street = get_field(address, "volledigAdres")
        street_name = get_field(address, "straatnaam")
        street_number = get_field(address,"postbusnummer")
        postcode = get_field(address,"postcode")
        land = get_field(address, "land")
        return street_name, street_number, postcode, land
    else:
        return None


r = requests.get(search_url)
resp = r.json()
for item in resp["resultaten"]:
    kvk_id = item["kvkNummer"]
    name = item["handelsnaam"] if "handelsnaam" in item.keys() else None
    address = get_address(kvk_id)
    print(kvk_id, name, address)
