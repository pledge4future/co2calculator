#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parse xmls downloaded from Probas database (https://www.probas.umweltbundesamt.de/php/index.php) to a table with
custom fields.

Hannah Weiser
h.weiser@stud.uni-heidelberg
Jan 2021
"""

import pandas as pd
import xml.etree.ElementTree as et
import glob

def read_xmls(id, filepath):
    """
    Function to parse Probas xml file of different PKW to a list of the values of interest (CO2-equivalent dependent
    on size class and fuel type

    :param id: unique sequential number
    :param filepath: path to XML file
    :return: list of desired values in the form ["id", "source", "model", "size_class", "fuel_type", "co2e"]
    """
    vals = pd.Series(index=range(6))
    xtree = et.parse(filepath)
    xroot = xtree.getroot()
    vals[0] = id
    for node in xroot:
        if node.tag == "name" and node.text != "PKW":
            # if not name "PKW" then size class has to be retrieved from name instead of entry
            # "Größenklasse / max. Beladung"
            if "klein" in node.text:
                vals[3] = "small" #or int: 0
            elif "mittel" in node.text:
                vals[3] = "medium" # or int: 1
            elif "gross" in node.text:
                vals[3] = "large" # or int: 2
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    vals[1] = child[0].text
                elif child.tag == "specificum":
                    vals[2] = child[0].text
        elif node.tag == "technical_data":
            for child in node:
                if child[0].text == "Größenklasse / max. Beladung":
                    vals[3] = child[1].text
                elif child[0].text == "Kraftstoff/Antrieb":
                    vals[4] = child[1].text
                #elif child[0].text == "Schadstoffklasse":
                #    vals[5] = child[1].text
                #elif child[0].text == "Straßenkategorie":
                #    vals[6] = child[1].text
        elif node.tag == "emissions_air":
            for child in node:
                if child[0].text == "CO2":
                    if child[3].tag == "sum":
                        vals[5] = child[3].text.replace(",",".")
    return vals.tolist()

infiles = glob.glob("probas_xmls/pkw/*.xml")

# read xmls
rows = []
for i, f in enumerate(infiles):
    rows.append(read_xmls(i, f))

# dataframe from nested list
cols = ["id", "source", "model", "size_class", "fuel_type", "co2e"]
out_df = pd.DataFrame(rows, columns=cols)

# rename some of the dataframe values
rename_dict = {
    "Durchschnittswert": "average",
    "Pkw 0-1,4 l": "small",
    "Pkw 1,4-2 l": "medium",
    "Pkw 2-9 l": "large",
    "Elektrizität": "electricity",
    "Erdgas-DE-CNG-2020": "cng",
    "Benzin": "gasoline",
    "Diesel": "diesel"
}
out_df.replace(rename_dict, inplace=True)

# change data type of id column to int64
out_df["id"] = out_df["id"].astype('int64')

# write to csv
outfile = "emission_factors_car.csv"
out_df.to_csv(outfile, index=False)