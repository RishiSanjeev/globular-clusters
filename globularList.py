#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# globularList.py
# Author: Rishi Sanjeev
# Created: 5-6-2025
# Description: Creates a list of visible Milky Way globular clusters based on location, light pollution, and instruments.

import requests
import math

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # raises exception if fetching fails
    return response.text.split("ellip")[2].split("_")[0].splitlines()

def selection_sort(orderableArr, complementaryArr):
    for i in range(len(orderableArr)-1):
        min_index = i
        for j in range(i+1, len(orderableArr)):
            if orderableArr[j] < orderableArr[min_index]:
                min_index = j
        orderableArr[i], orderableArr[min_index] = orderableArr[min_index], orderableArr[i]
        complementaryArr[i], complementaryArr[min_index] = complementaryArr[min_index], complementaryArr[i]

def limitingMagGenerator(zero_point, subexposureTime, subexposureTimeReference, apertureArea, apertureAreaReference, systemSensitivity, systemSensitivityReference, exposureCount):
    return (1.25 * math.log10(exposureCount)) + zero_point + 2.5 * math.log10(subexposureTime/subexposureTimeReference) + 2.5 * math.log10(apertureArea/apertureAreaReference) + 2.5 * math.log10(systemSensitivity/systemSensitivityReference)

url = "https://physics.mcmaster.ca/~harris/mwgc.dat"
data_lines = fetch_data(url)

singleWords = ['Eridanus','Pyxis','1636-283','2MS-GC01','ESO-SC06','2MS-GC02','GLIMPSE01','GLIMPSE02']
appVMag = []
globularClusters = []

for line in data_lines:
    if line == '':
        continue
    elif line.split()[0] in singleWords:
        if len(line.split()) < 7:
            continue
        try:
            appVMag.append(float(line.split()[6]))
            globularClusters.append(line.split()[0])
        except IndexError:
            print(line.split())
        continue
    try:
        appVMag.append(float(line.split()[7]))
        globularClusters.append(line.split()[0]+' '+line.split()[1])
    except IndexError:
        print(line.split())

selection_sort(appVMag,globularClusters)

orderedList = []

limitingMag = limitingMagGenerator(17.5,15,1,506.7,100,0.4,1,240)

for k in range(len(globularClusters)):
    if appVMag[k] < limitingMag:
        orderedList.append(globularClusters[k]+', '+str(appVMag[k]))
        continue
    break

print('\n'.join(orderedList))
