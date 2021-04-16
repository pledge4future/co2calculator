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
import os

def read_xmls_mobility(id, filepath, co2e_df):
    """
    Function to parse Probas xml file of different PKW to a list of the values of interest (CO2-equivalent dependent
    on size class and fuel type

    :param id: unique sequential number
    :param filepath: path to XML file

    :return: appended dataframe
    """
    xtree = et.parse(filepath)
    filepath = os.path.normpath(filepath)
    folder = filepath.split(os.sep)[-2]
    xroot = xtree.getroot()
    unit = None
    if folder == "car":
        co2e_df.loc[id, "category"] = "vehicle"
    elif folder == "bus" or folder == "train":
        co2e_df.loc[id, "category"] = "public transport"
    co2e_df.loc[id, "subcategory"] = folder
    for node in xroot:
        if node.tag == "name":
            co2e_df.loc[id, "name"] = node.text
            # if not name "PKW" then size class has to be retrieved from name instead of entry
            # "Größenklasse / max. Beladung"
            if "klein" in node.text or "mini" in node.text:
                co2e_df.loc[id, "size_class"] = "small" #or int: 0
            elif "mittel" in node.text:
                co2e_df.loc[id, "size_class"] = "medium" # or int: 1
            elif "gross" in node.text:
                co2e_df.loc[id, "size_class"] = "large" # or int: 2
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[id, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[id, "model"] = child[0].text
        elif node.tag == "technical_data":
            for child in node:
                if child[0].text == "Größenklasse / max. Beladung":
                    co2e_df.loc[id, "size_class"] = child[1].text
                elif child[0].text == "Kraftstoff/Antrieb":
                    co2e_df.loc[id, "fuel_type"] = child[1].text
                elif child[0].text == "Auslastungsgrad":
                    co2e_df.loc[id, "occupancy"] = child[1].text
                elif child[0].text == "Kapazität":
                    co2e_df.loc[id, "capacity"] = child[1].text.replace(",", ".")
                #elif child[0].text == "Schadstoffklasse":
                #    vals[5] = child[1].text
                #elif child[0].text == "Straßenkategorie":
                #    vals[6] = child[1].text
        elif node.tag == "outputs":
            for child in node:
                if child[3].tag == "unit":
                    unit = child[3].text
        elif node.tag == "emissions_air":
            for child in node:
                if child[0].text == "CO2":
                    if not unit:
                        unit = "P.km"
                    if child[3].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
        elif node.tag == "emissions_air_aggregated":
            for child in node:
                if child[0].text == "CO2-Äquivalent":
                    if not unit:
                        unit = "P.km"
                    if child[3].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[id, "unit"] = unit
    co2e_df.loc[id, "co2e_unit"] = unit_co2e
    return co2e_df


def read_xmls_electricity(id, filepath, co2e_df):
    xtree = et.parse(filepath)
    xroot = xtree.getroot()
    co2e_df.loc[id, "category"] = "electricity"
    for node in xroot:
        if node.tag == "name":
            co2e_df.loc[id, "name"] = node.text
            if "Solar" in node.text:
                co2e_df.loc[id, "subcategory"] = "solar"
            elif "KW" in node.text:
                co2e_df.loc[id, "subcategory"] = "german energy mix"
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[id, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[id, "model"] = child[0].text
        elif node.tag == "outputs":
            for child in node:
                if child[3].tag == "unit":
                    unit = child[3].text
        elif node.tag == "emissions_air_aggregated":
            for child in node:
                if child[0].text == "CO2-Äquivalent":
                    if child[2].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[2].text.replace(",", ".")
                    elif child[3].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[id, "unit"] = unit
    co2e_df.loc[id, "co2e_unit"] = unit_co2e

    return co2e_df


def read_xmls_heating(id, filepath, co2e_df):
    xtree = et.parse(filepath)
    xroot = xtree.getroot()
    co2e_df.loc[id, "category"] = "heating"
    for node in xroot:
        if node.tag == "name":
            if node.tag == "name":
                co2e_df.loc[id, "name"] = node.text
            if "Braunkohle" in node.text:
                co2e_df.loc[id, "fuel_type"] = "coal"
            elif "Fernwärme" in node.text:
                co2e_df.loc[id, "fuel_type"] = "district_heating"
            elif "El-Heizung" in node.text:
                co2e_df.loc[id, "fuel_type"] = "electricity"
            elif "Gas-Heizung" in node.text:
                co2e_df.loc[id, "fuel_type"] = "gas"
            elif "mono-Luft" in node.text:
                co2e_df.loc[id, "fuel_type"] = "heatpump_air"
            elif "mono-Erdreich" in node.text:
                co2e_df.loc[id, "fuel_type"] = "heatpump_ground"
            elif "mono-Wasser" in node.text:
                co2e_df.loc[id, "fuel_type"] = "heatpump_water"
            elif "Flüssiggas" in node.text:
                co2e_df.loc[id, "fuel_type"] = "liquid_gas"
            elif "Öl-Heizung" in node.text:
                co2e_df.loc[id, "fuel_type"] = "oil"
            elif "Pellet" in node.text:
                co2e_df.loc[id, "fuel_type"] = "pellet"
            elif "SolarKollektor" in node.text:
                co2e_df.loc[id, "fuel_type"] = "solar"
            elif "Hackschnitzel" in node.text:
                co2e_df.loc[id, "fuel_type"] = "woodchips"
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[id, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[id, "model"] = child[0].text
        elif node.tag == "outputs":
            for child in node:
                if child[3].tag == "unit":
                    unit = child[3].text
        elif node.tag == "emissions_air_aggregated":
            for child in node:
                if child[0].text == "CO2-Äquivalent":
                    if child[2].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[2].text.replace(",", ".")
                    elif child[3].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[id, "unit"] = unit
    co2e_df.loc[id, "co2e_unit"] = unit_co2e

    return co2e_df


def read_xmls_planes(id, filepath, co2e_df):
    xtree = et.parse(filepath)
    filepath = os.path.normpath(filepath)
    folder = filepath.split(os.sep)[-2]
    xroot = xtree.getroot()
    co2e_df.loc[id, "category"] = "public transport"
    co2e_df.loc[id, "subcategory"] = folder
    for node in xroot:
        if node.tag == "name":
            if node.tag == "name":
                co2e_df.loc[id, "name"] = node.text
            if "international" in node.text:
                co2e_df.loc[id, "range"] = "international"
            if "Inland" in node.text:
                co2e_df.loc[id, "range"] = "inland"
            co2e_df.loc[id, "name"] = node.text
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[id, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[id, "model"] = child[0].text
        elif node.tag == "technical_data":
            for child in node:
                if child[0].text == "Besetzungsgrad":
                    co2e_df.loc[id, "occupancy"] = child[1].text
        elif node.tag == "outputs":
            for child in node:
                if child[3].tag == "unit":
                    unit = child[3].text
        elif node.tag == "emissions_air_aggregated":
            for child in node:
                if child[0].text == "CO2-Äquivalent":
                    if child[2].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[2].text.replace(",", ".")
                    elif child[3].tag == "sum":
                        co2e_df.loc[id, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[id, "unit"] = unit
    co2e_df.loc[id, "co2e_unit"] = unit_co2e

    return co2e_df


def append_from_csv(filepath, df):
    new_df = pd.read_csv(filepath, sep=",")
    print(new_df)
    df = df.append(new_df, ignore_index=True)

    return df


def rename_reformat_df(df, dict):
    df.replace(dict, inplace=True)

    return df

infiles = glob.glob("probas_xmls/*/*.xml")
print(infiles)

df = pd.DataFrame([], columns=["category", "subcategory", "source", "model", "name", "unit", "size_class", "occupancy", "capacity", "range", "fuel_type", "co2e_unit", "co2e"])
# read xmls
for id, f in enumerate(infiles):
    f = os.path.normpath(f)
    folder = f.split(os.sep)[-2]
    if folder == "car" or folder == "train" or folder == "bus":
        df = read_xmls_mobility(id, f, df)
    elif folder == "plane":
        df = read_xmls_planes(id, f, df)
    elif folder == "electricity":
        df = read_xmls_electricity(id, f, df)
    elif folder == "heating":
        df = read_xmls_heating(id, f, df)

print(df)

other_files = glob.glob("other_sources/*.csv")
for file in other_files:
    df = append_from_csv(file, df)

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
    "Reisebus 3,5-18 t": "medium",
    "km": "P.km",
    "kg/km": "kg/P.km"
}
df = rename_reformat_df(df, rename_dict)
print(df)

outfile = "emission_factors.csv"
df.to_csv(outfile)
