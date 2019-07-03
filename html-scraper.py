from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import requests
import re

rightmove_search_page = "https://www.rightmove.co.uk/property-to-rent.html"

# Search params
min_price = 700
max_price = 1100
bedrooms = 2
prop_type = "flats"

properties = []

pgnum = 0
numpp = 24

# Gather
while (pgnum < 6):
    searchpage = requests.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE%5E1585&maxBedrooms=" + str(bedrooms) +
                              "&minBedrooms=" + str(bedrooms) + "&maxPrice=" + str(max_price) + "&minPrice=" + str(min_price) + "&index=" +
                              str(pgnum * numpp) + "&propertyTypes=flat&primaryDisplayPropertyType=flats&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=")

    properties.extend(set(re.findall('\d{8}', searchpage.text)))

    pgnum += 1


# Test appropriateness
def isAppropriate(text):
    text = text.lower()
    if ("parking" not in text):
        raise NoParkingException()
    if ("no parking" in text):
        raise NoParkingException()
    if ("balcony" not in text):
        raise NoBalconyException()
    if ("juliette" in text or "juliet" in text):
        raise JulietteException()


class NoBalconyException(Exception):
    def __init__(self):
        super().__init__("No balcony")


class JulietteException(Exception):
    def __init__(self):
        super().__init__("Juliette balcony")


class NoParkingException(Exception):
    def __init__(self):
        super().__init__("No parking")


class AlreadySavedException(Exception):
    def __init__(self):
        super().__init__("Already saved")


suitable = []
for p in properties:
    prop = requests.get(
        "https://www.rightmove.co.uk/property-to-rent/property-" + p + ".html").text
    try:
        isAppropriate(prop)
        # Property is appropriate, attempt save
        try:
            # Get to button html
            r1 = re.search("(?<=property-actions-save)(?s)(.*$)", prop)

            if r1 is not None:
                # Get link from button element
                r2 = re.search(
                    "(href=\")(.*?)\"", r1.group())
                if r2 is not None:
                    like_link = r2.group()[6:][:1]
                    if (len(like_link) < 1000):
                        print("FOUND: " + prop)
                        requests.get(like_link)
                        suitable.extend(prop)
        except Exception as e:
            print("    " + str(e))
            raise AlreadySavedException()
    except Exception as e:
        print("    " + str(e))

print(suitable)
