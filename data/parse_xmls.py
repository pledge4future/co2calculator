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
    :return: list of desired values in the form ["id", "source", "model", "size_class", "fuel_type", "capacity", "occupancy", "co2e"]
    """
    vals = pd.Series(index=range(8))
    xtree = et.parse(filepath)
    xroot = xtree.getroot()
    vals[0] = id
    for node in xroot:
        if node.tag == "name":
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
                elif child[0].text == "Auslastungsgrad":
                    vals[6] = child[1].text
                elif child[0].text == "Kapazität":
                    vals[5] = child[1].text.replace(",", ".")
                #elif child[0].text == "Schadstoffklasse":
                #    vals[5] = child[1].text
                #elif child[0].text == "Straßenkategorie":
                #    vals[6] = child[1].text
        elif node.tag == "emissions_air":
            for child in node:
                if child[0].text == "CO2":
                    if child[3].tag == "sum":
                        vals[7] = child[3].text.replace(",",".")
    return vals.tolist()


def rename_reformat_df(df, dict):
    df.replace(dict, inplace=True)
    # change data type of id column to int64
    df["id"] = df["id"].astype('int64')
    return df


# 1. parse car xmls
infiles_car = glob.glob("probas_xmls/pkw/*.xml")
infiles_train = glob.glob("probas_xmls/train/*.xml")
infiles_bus = glob.glob("probas_xmls/bus/Reisebus*.xml")
cols = ["id", "source", "model", "size_class", "fuel_type", "capacity", "occupancy", "co2e"]

# read xmls
rows = []
for i, f in enumerate(infiles_car):
    rows.append(read_xmls(i, f))
# dataframe from nested list
car_df = pd.DataFrame(rows, columns=cols)
car_df.drop(["capacity", "occupancy"], axis=1, inplace=True)

rows = []
for i, f in enumerate(infiles_train):
    rows.append(read_xmls(i, f))
train_df = pd.DataFrame(rows, columns=cols)
train_df.drop(["size_class", "capacity", "occupancy"], axis=1, inplace=True)

rows = []
for i, f in enumerate(infiles_bus):
    rows.append(read_xmls(i, f))
bus_df = pd.DataFrame(rows, columns=cols)

rename_dict = {
    "Durchschnittswert": "average",
    "Pkw 0-1,4 l": "small",
    "Pkw 1,4-2 l": "medium",
    "Pkw 2-9 l": "large",
    "Elektrizität": "electric",
    "Elektrisch": "electric",
    "Erdgas-DE-CNG-2020": "cng",
    "Benzin": "gasoline",
    "Diesel": "diesel",
    "Reisebus 18-30 t": "large",
    "Reisebus 3,5-18 t": "medium"
}
car_df = rename_reformat_df(car_df, rename_dict)
train_df = rename_reformat_df(train_df, rename_dict)
bus_df = rename_reformat_df(bus_df, rename_dict)

# write to csv
outfile_car = "emission_factors_car.csv"
car_df.to_csv(outfile_car, index=False)
outfile_train = "emission_factors_train.csv"
train_df.to_csv(outfile_train, index=False)
outfile_bus = "emission_factors_bus.csv"
bus_df.to_csv(outfile_bus, index=False)