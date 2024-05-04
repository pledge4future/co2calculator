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


def read_xmls_mobility(idx, filepath, co2e_df):
    """
    Function to write emission factors from Probas xml files for different modes of transport to an emission factor
    dataframe

    :param idx: unique sequential number
    :param filepath: path to XML file
    :param co2e_df: existing dataframe, to which the emission factors that are read from the XMLs are appended

    :return: appended dataframe
    """
    xtree = et.parse(filepath)
    filepath = os.path.normpath(filepath)
    folder = filepath.split(os.sep)[-2]
    xroot = xtree.getroot()
    unit = None
    if folder == "car":
        co2e_df.loc[idx, "category"] = "vehicle"
    elif folder == "bus" or folder == "train":
        co2e_df.loc[idx, "category"] = "public_transport"
    co2e_df.loc[idx, "subcategory"] = folder
    for node in xroot:
        if node.tag == "name":
            co2e_df.loc[idx, "name"] = node.text
            # if not name "PKW" then size class has to be retrieved from name instead of entry
            # "Größenklasse / max. Beladung"
            if "klein" in node.text or "mini" in node.text:
                co2e_df.loc[idx, "size_class"] = "small"
            elif "mittel" in node.text:
                co2e_df.loc[idx, "size_class"] = "medium"
            elif "gross" in node.text:
                co2e_df.loc[idx, "size_class"] = "large"
            # for bus and train, get the "range" (i.e., long-distance vs. local) from name
            elif "Reise" in node.text or "fern" in node.text or "Fern" in node.text:
                co2e_df.loc[idx, "range"] = "long-distance"
            elif "nah" in node.text or "Nah" in node.text:
                co2e_df.loc[idx, "range"] = "local"
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[idx, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[idx, "model"] = child[0].text
        elif node.tag == "technical_data":
            for child in node:
                if child[0].text == "Größenklasse / max. Beladung":
                    co2e_df.loc[idx, "size_class"] = child[1].text
                elif child[0].text == "Kraftstoff/Antrieb":
                    co2e_df.loc[idx, "fuel_type"] = child[1].text
                elif child[0].text == "Auslastungsgrad":
                    co2e_df.loc[idx, "occupancy"] = child[1].text
                elif child[0].text == "Besetzungsgrad":
                    co2e_df.loc[idx, "occupancy"] = child[1].text
                elif child[0].text == "Kapazität":
                    co2e_df.loc[idx, "capacity"] = child[1].text.replace(",", ".")
                # elif child[0].text == "Schadstoffklasse":
                #     co2e_df.loc[id, "Schadstoffklasse"] = child[1].text
                elif (
                    child[0].text == "Straßenkategorie" and child[1].text == "innerorts"
                ):
                    co2e_df.loc[idx, "range"] = "local"
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
                        co2e_df.loc[idx, "co2e"] = child[3].text.replace(",", ".")
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
                        co2e_df.loc[idx, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[idx, "unit"] = unit
    co2e_df.loc[idx, "co2e_unit"] = unit_co2e

    return co2e_df


def read_xmls_electricity(idx, filepath, co2e_df):
    """
    Function to write emission factors from Probas xml files for electricity sources to an emission factor
    dataframe

    :param idx: unique sequential number
    :param filepath: path to XML file
    :param co2e_df: existing dataframe, to which the emission factors that are read from the XMLs are appended

    :return: appended dataframe
    """
    xtree = et.parse(filepath)
    xroot = xtree.getroot()
    co2e_df.loc[idx, "category"] = "electricity"
    for node in xroot:
        if node.tag == "name":
            co2e_df.loc[idx, "name"] = node.text
            if "Solar" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "solar"
            elif "KW" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "german_energy_mix"
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[idx, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[idx, "model"] = child[0].text
        elif node.tag == "outputs":
            for child in node:
                if child[3].tag == "unit":
                    unit = child[3].text
        elif node.tag == "emissions_air_aggregated":
            for child in node:
                if child[0].text == "CO2-Äquivalent":
                    if child[2].tag == "sum":
                        co2e_df.loc[idx, "co2e"] = child[2].text.replace(",", ".")
                    elif child[3].tag == "sum":
                        co2e_df.loc[idx, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[idx, "unit"] = unit
    co2e_df.loc[idx, "co2e_unit"] = unit_co2e

    return co2e_df


def read_xmls_heating(idx, filepath, co2e_df):
    """
    Function to write emission factors from Probas xml files for different heating types to an emission factor
    dataframe

    :param idx: unique sequential number
    :param filepath: path to XML file
    :param co2e_df: existing dataframe, to which the emission factors that are read from the XMLs are appended

    :return: appended dataframe
    """
    xtree = et.parse(filepath)
    xroot = xtree.getroot()
    co2e_df.loc[idx, "category"] = "heating"
    for node in xroot:
        if node.tag == "name":
            if node.tag == "name":
                co2e_df.loc[idx, "name"] = node.text
            if "Braunkohle" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "coal"
            elif "Fernwärme" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "district_heating"
            elif "El-Heizung" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "electricity"
            elif "Gas-Heizung" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "gas"
            elif "mono-Luft" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "heat_pump_air"
            elif "mono-Erdreich" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "heat_pump_ground"
            elif "mono-Wasser" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "heat_pump_water"
            elif "Flüssiggas" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "liquid_gas"
            elif "Öl-Heizung" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "oil"
            elif "Pellet" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "pellet"
            elif "SolarKollektor" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "solar"
            elif "Hackschnitzel" in node.text:
                co2e_df.loc[idx, "fuel_type"] = "woodchips"
        elif node.tag == "meta":
            for child in node:
                if child.tag == "source":
                    co2e_df.loc[idx, "source"] = child[0].text
                elif child.tag == "specificum":
                    co2e_df.loc[idx, "model"] = child[0].text
        elif node.tag == "outputs":
            for child in node:
                if child[3].tag == "unit":
                    unit = child[3].text
        elif node.tag == "emissions_air_aggregated":
            for child in node:
                if child[0].text == "CO2-Äquivalent":
                    if child[2].tag == "sum":
                        co2e_df.loc[idx, "co2e"] = child[2].text.replace(",", ".")
                    elif child[3].tag == "sum":
                        co2e_df.loc[idx, "co2e"] = child[3].text.replace(",", ".")
                    if child[3].tag == "unit":
                        unit_co2e = child[3].text + "/" + unit
                    elif child[4].tag == "unit":
                        unit_co2e = child[4].text + "/" + unit
    co2e_df.loc[idx, "unit"] = unit
    co2e_df.loc[idx, "co2e_unit"] = unit_co2e

    return co2e_df


# def read_xmls_planes(idx, filepath, co2e_df):
#    """
#    Function to write emission factors from Probas xml files for planes to an emission factor dataframe
#
#    :param idx: unique sequential number
#    :param filepath: path to XML file
#    :param co2e_df: existing dataframe, to which the emission factors that are read from the XMLs are appended
#
#    :return: appended dataframe
#    """
#    xtree = et.parse(filepath)
#    filepath = os.path.normpath(filepath)
#    folder = filepath.split(os.sep)[-2]
#    xroot = xtree.getroot()
#    co2e_df.loc[idx, "category"] = "public transport"
#    co2e_df.loc[idx, "subcategory"] = folder
#    for node in xroot:
#        if node.tag == "name":
#            if node.tag == "name":
#                co2e_df.loc[idx, "name"] = node.text
#            if "international" in node.text:
#                co2e_df.loc[idx, "range"] = "international"
#            if "Inland" in node.text:
#                co2e_df.loc[idx, "range"] = "inland"
#            co2e_df.loc[idx, "name"] = node.text
#        elif node.tag == "meta":
#            for child in node:
#                if child.tag == "source":
#                    co2e_df.loc[idx, "source"] = child[0].text
#                elif child.tag == "specificum":
#                    co2e_df.loc[idx, "model"] = child[0].text
#        elif node.tag == "technical_data":
#            for child in node:
#                if child[0].text == "Besetzungsgrad":
#                    co2e_df.loc[idx, "occupancy"] = child[1].text
#        elif node.tag == "outputs":
#            for child in node:
#                if child[3].tag == "unit":
#                    unit = child[3].text
#        elif node.tag == "emissions_air_aggregated":
#            for child in node:
#                if child[0].text == "CO2-Äquivalent":
#                    if child[2].tag == "sum":
#                        co2e_df.loc[idx, "co2e"] = child[2].text.replace(",", ".")
#                    elif child[3].tag == "sum":
#                        co2e_df.loc[idx, "co2e"] = child[3].text.replace(",", ".")
#                    if child[3].tag == "unit":
#                        unit_co2e = child[3].text + "/" + unit
#                    elif child[4].tag == "unit":
#                        unit_co2e = child[4].text + "/" + unit
#    co2e_df.loc[idx, "unit"] = unit
#    co2e_df.loc[idx, "co2e_unit"] = unit_co2e
#
#    return co2e_df


def append_from_csv(filepath, df):
    """
    Function to read a csv to dataframe and append to existing dataframe

    :param filepath: path of .csv-file
    :param df: exiting dataframe

    :return: appended dataframe
    """
    new_df = pd.read_csv(filepath, sep=";")
    df = df.append(new_df, ignore_index=True)

    return df


def rename_reformat_df(df, dictionary):
    df.replace(dictionary, inplace=True)

    return df


infiles = glob.glob("probas_xmls/*/*.xml")

df = pd.DataFrame(
    [],
    columns=[
        "category",
        "subcategory",
        "source",
        "model",
        "name",
        "unit",
        "size_class",
        "occupancy",
        "capacity",
        "range",
        "fuel_type",
        "co2e_unit",
        "co2e",
    ],
)
# read xmls
for i, f in enumerate(infiles):
    f = os.path.normpath(f)
    folder = f.split(os.sep)[-2]
    if folder == "car" or folder == "train" or folder == "bus":
        df = read_xmls_mobility(i, f, df)
    # elif folder == "plane":
    #    df = read_xmls_planes(i, f, df)
    elif folder == "electricity":
        df = read_xmls_electricity(i, f, df)
    elif folder == "heating":
        df = read_xmls_heating(i, f, df)

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
    "Linienbus 18-30 t": "large",
    "Linienbus 15-18 t": "medium",
    "Linienbus 3,5-15 t": "small",
    "km": "P.km",
    "kg/km": "kg/P.km",
    "H2 (energetisch)": "hydrogen",
    "electricity-CZ-transport": "electric",
}
df = rename_reformat_df(df, rename_dict)

outfile = "emission_factors.csv"
df.to_csv(outfile)
