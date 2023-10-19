# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:16:36 2023

@author: Titus
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import numpy as np

#%% Read the OH and CO3 cards

f_name = (os.listdir('Cards'))
f_howmany = range(len(f_name))

df = pd.DataFrame(columns=['PDF#', 'Formula', '(003)', '(006)', 'Ref'], index=f_howmany) #df with headers for info you are collecting

for x in f_howmany:
    Card = pd.read_csv(os.path.join('Cards', f_name[x]), sep=':', header=None, names=range(3), index_col=False, nrows=23) #reads card as : seperated

    #gets pdf number from first line of card
    first_line = Card.iloc[0,0]
    start_bracket = first_line.find("[")
    end_bracket = first_line.find("]")
    df.at[x, 'PDF#']= first_line[start_bracket + 1:end_bracket]
    
    df.at[x, 'Formula'] = Card.iloc[2, 1]
    
    #Reads the patern data from end of card
    Patern = pd.read_csv(os.path.join('Cards', f_name[x]), sep='\t', skiprows=25, skipfooter=1, header=1, engine='python')
    
    df.at[x, '(003)'] = Patern.loc[0, 'd(Å)']
    df.at[x, '(006)'] = Patern.loc[1, 'd(Å)']
    
    df.at[x, 'Ref'] = Card.iloc[11, 1]
    
# df.to_csv('Output/HT_Co3_and_OH.csv')

#%% Read the NO3

f_name = (os.listdir('Cards_NO3'))
f_howmany = range(len(f_name))

NO3 = pd.DataFrame(columns=['PDF#', 'Formula', '(003)', '(006)', 'Ref'], index=f_howmany) #df with headers for info you are collecting

for x in f_howmany:
    Card = pd.read_csv(os.path.join('Cards_NO3', f_name[x]), sep=':', header=None, names=range(3), index_col=False, nrows=23) #reads card as : seperated

    #gets pdf number from first line of card
    first_line = Card.iloc[0,0]
    start_bracket = first_line.find("[")
    end_bracket = first_line.find("]")
    NO3.at[x, 'PDF#']= first_line[start_bracket + 1:end_bracket]
    
    NO3.at[x, 'Formula'] = Card.iloc[2, 1]
    
    #Reads the patern data from end of card
    Patern = pd.read_csv(os.path.join('Cards_NO3', f_name[x]), sep='\t', skiprows=25, skipfooter=1, header=1, engine='python')
    
    NO3.at[x, '(003)'] = Patern.loc[0, 'd(Å)']
    NO3.at[x, '(006)'] = Patern.loc[1, 'd(Å)']
    
    NO3.at[x, 'Ref'] = Card.iloc[11, 1]
    
# NO3.to_csv('Output/HT_NO3.csv')
    
#%% seperating OH and CO3 version

HT_index = []
Mex_index = []
HT = df
Mex = df
# HT = pd.DataFrame() #columns=['PDF#', 'Formula', '(003)', '(006)', 'Ref'])
# Mex = pd.DataFrame() #columns=['PDF#', 'Formula', '(003)', '(006)', 'Ref'])
for index, row in df.iterrows():
    formula = row['Formula']
    if 'C' in formula:
        HT_index.append(index)
        Mex = Mex.drop(index)
    else:
        Mex_index.append(index)
        HT = HT.drop(index)
       
    

#%% plot the values
plt.style.use('Inputs/publish2.mplstyle')
fig, ax = plt.subplots()

ax.scatter(HT['(003)'], HT['(006)'], marker='x', label='Hydrotalcite')
ax.scatter(Mex['(003)'], Mex['(006)'], marker='+', label='Meixnerite')
ax.scatter(NO3['(003)'], NO3['(006)'], marker='2', label='NO3-HT')
# ax.set_xlim([7.3,8])
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
# ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(MultipleLocator(0.05))
ax.xaxis.set_minor_locator(MultipleLocator(0.05))

ax.set_xlabel("(003) d-space (Å)")
ax.set_ylabel("(006) d-space (Å)")
ax.legend()
fig.savefig('Plots/Washed_5day_31P_NMR.svg', transparent=False, bbox_inches="tight")

#%% stats

x = HT['(003)']
name = 'HT'
def Stats(x, name):
    print(name)
    print('Mean = ', np.average(x))
    print('standard deviation = ', np.std(x))
    print('Range = [', np.min(x), ' - ', np.max(x), ']')
    
Stats(HT['(003)'], 'Hydrotalcite')
Stats(Mex['(003)'], 'Meixnerite')
Stats(NO3['(003)'], 'NO3-LDH')





