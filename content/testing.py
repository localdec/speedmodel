# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 07:58:42 2020

@author: Michael Brydon

Testing routines
"""

import localdec
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import math


# load pipeline spreadsheet
data_dir = "../SpeedData"
dist_col = 3
pls = pd.read_excel(data_dir + "/" +  "Datasets.xlsx")
pls["Pipeline"] = pls["Filename"].str.extract("^(.*)\sVelocity.*")
pls.set_index("Pipeline", inplace=True)

# read tool data into a dictionary for later use
pipelines = dict()
colheads = [x.group(1) for x in [re.match("(^SpeedData\d)", col) for col in pls.columns] if x != None]
toolheads = [x.group(1) for x in [re.match("(^Tool\d)", col) for col in pls.columns] if x != None]
for pl in pls.index:
    pipeline = dict()
    tools=dict()
    i = 0
    for toolhead in toolheads:
        if pls.loc[pl, toolhead] == pls.loc[pl, toolhead]:
            tcol = {"column": int(pls.loc[pl, colheads[i]])}
            toolname = re.match("^Velocity\s*\(\d{4}(.*)\)$", pls.loc[pl, toolhead]).group(1).strip().upper()
            tools[toolname] = tcol
            i += 1
    pipeline["tools"] = tools
    pipelines[pl] = pipeline
    
# read data for a particular pipeline
pl = "NIC_FRA_610"
cols = [dist_col] + [tool[1]["column"] for tool in pipelines[pl]["tools"].items()]
col_names = ["Distance"] +  [tool[0] for tool in pipelines[pl]["tools"].items()]
data_skiprows = [i for i in range(4)]
if not math.isnan(pls.loc[pl, "Skip"]):
    data_skiprows.append(int(pls.loc[pl, "Skip"]))
print(pl)
pl_raw = pd.read_excel(data_dir + "/" + pls.loc[pl, "Filename"],
               sheet_name=pls.loc[pl, "Sheet"],
               usecols=cols,
               names = col_names,
               skiprows=data_skiprows)

# unpivot data
pl = pd.melt(pl_raw,
                id_vars="Distance",
                var_name="Tool",
                value_name="Velocity")
pl["Tool"] = pl["Tool"].astype('category')

# speed profile
plt.figure(figsize=(16,8))
ax = sns.lineplot(x="Distance", y="Velocity", hue="Tool", data=pl)
ax.set(xlabel="distance", ylabel="tool speed")
plt.show()

#m mark excursions
pl["Excursion"] = 0  # reset column
dist_thresh = 100
tool = "ROSEN MFL-C"
localdec.mark_excursion(tool, 3.6, dist_thresh, pl)

# count excursions
print(pl.groupby("Tool").get_group(tool)["Excursion"].sum())
print(pl.groupby("Tool").get_group(tool)["Length"].mean())

