from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re

rightmove_search_page = "https://www.rightmove.co.uk/property-to-rent.html"

# Search params
min_price = 700
max_price = 1100
bedrooms = 2
prop_type = "flats"

options = webdriver.ChromeOptions()

options.add_argument(
    "user-data-dir=C:\\Users\\Camer\\AppData\\Local\\Google\\Chrome\\User Data")
driver = webdriver.Chrome(
    executable_path=r".\chromedriver.exe", options=options)
driver.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE%5E1585&maxBedrooms=" + str(bedrooms) +
           "&minBedrooms=" + str(bedrooms) + "&maxPrice=" + str(max_price) + "&minPrice=" + str(min_price) + "&propertyTypes=flat&primaryDisplayPropertyType=flats&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=")

# CRAWL---------------------------------------------------------------
pgnum = 0
numpp = 24
all_props = []
potential_properties = []


def pop():
    try:
        driver.execute_script('eDRLayer.hide()')
    except:
        pass


while pgnum < 4:
    print("yeet")
    props = driver.find_elements_by_partial_link_text('2 bedroom')

    for p in props:
        all_props.append(p.get_attribute('href'))
        pop()

    # Next page
    pgnum += 1
    driver.get("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=OUTCODE%5E1585&maxBedrooms=" + str(bedrooms) +
               "&minBedrooms=" + str(bedrooms) + "&maxPrice=" + str(max_price) + "&minPrice=" + str(min_price) + "&index=" +
               str(pgnum * numpp) + "&propertyTypes=flat&primaryDisplayPropertyType=flats&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=")

# ESTABLISH APPROPRITENESS----------------------------------------------------------------------------


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


for p in set(all_props):
    driver.get(p)
    text = driver.page_source
    print("Inspecting property: " + p)
    try:
        isAppropriate(text)
        # Property is appropriate, attempt save
        try:
            driver.find_element_by_class_name(
                "registersource-save-property").click()
            print("NEW PROPERTY FOUND!!")
        except:
            raise AlreadySavedException()
    except Exception as e:
        print("    " + str(e))
