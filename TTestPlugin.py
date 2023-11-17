#!/usr/bin/env python
# coding: utf-8

# In[14]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sympy.interactive import printing
printing.init_printing(use_latex=True)
sns.set(rc={'figure.figsize':(8,6)})
from IPython.display import Image
import os
import numpy as np
from scipy import stats
import csv
all_colors=["orange", "blue","red","black","#2ecc71", "#2e0071",  "#2efdaa"]
subset_colors =  ["red","black","#2ecc71", "#2e0071",  "#2efdaa", "#200daa","#2ffd00"]
include_plots = ['arc','alecar3']
import os.path as path
import xlwt 
from xlwt import Workbook 


# In[36]:


def writeHeader(sheet1, our_algo, other_algo):
    row = 0
    col= 1
    sheet1.write(row, col, "dataset") 
    col= col+ 1
    sheet1.write(row, col,  "algorithm")
    col= col+ 1
    sheet1.write(row, col,   "cache_size") 
    col= col+ 1
    sheet1.write(row, col, "our_algo_mean") 
    col= col+ 1
    sheet1.write(row, col, "other_algo_mean") 
    col= col+ 1
    sheet1.write(row, col, "other_algo_std") 
    col= col+ 1 
    sheet1.write(row,  col,  "other_algo_std") 
    col= col+ 1 
    sheet1.write(row,col , "p-value")
    col= col+ 1 
    sheet1.write(row, col,  "color") 
    
def writeInCsv(sheet1,row, df_cache, our_algo, other_algo, datas, cache_size):
    t2, p2  = stats.ttest_rel(df_cache[our_algo], df_cache[other_algo])
#             df_cache[['ALeCaR', 'ScanALeCaR']].plot(kind='box')
    our_algo_mean = np.mean(np.array(df_cache[our_algo]))
    other_algo_mean = np.mean(np.array(df_cache[other_algo]))
    # Calculate the standard deviation
    our_algo_std = np.std(np.array(df_cache[our_algo]))
    other_algo_std = np.std(np.array(df_cache[other_algo]))

    other_algo_std =  stats.sem(np.array(df_cache[our_algo]))
    other_algo_std =  stats.sem(np.array(df_cache[other_algo]))
    print( "*****Dataset:" , datas , "*****Cache Size:" , cache_size , "*******")
    print( our_algo ," Average = " , our_algo_mean, "Standard deviation = " , our_algo_std)
    print(other_algo, " Average = " , other_algo_mean, "Standard deviation = " ,other_algo_std)

    print("t-test with respect to", other_algo)
    print("t = " + str(t2))
    print("p-value = " + str(p2))

    color = 0 if p2>0.05  else (1 if our_algo_mean> other_algo_mean  else -1)

    col= 1
    sheet1.write(row, col, datas) 
    col= col+ 1
    sheet1.write(row, col,  other_algo)
    col= col+ 1
    sheet1.write(row, col,   cache_size) 
    col= col+ 1
    sheet1.write(row, col, our_algo_mean) 
    col= col+ 1
    sheet1.write(row, col, other_algo_mean) 
    col= col+ 1
    sheet1.write(row, col, other_algo_std) 
    col= col+ 1 
    sheet1.write(row,  col,  other_algo_std) 
    col= col+ 1 
    sheet1.write(row,col , round(p2,3))
    col= col+ 1 
    sheet1.write(row, col,  color) 
    
    


# In[38]:

class TTestPlugin:
 def input(self, inputfile):
  self.infile = inputfile
  self.df = pd.read_excel(inputfile)
 def run(self):
     pass
 def output(self, outputfile):
  our_algo = "ScanALeCaR"
  other_algos = [ 'ARC', "LIRS", "DLIRS", "LeCaR", "ALeCaR2N", "ALeCaRN"]


  our_algo = "ALeCaRN"
  other_algos = [ 'ARC', "LIRS", "DLIRS", "LeCaR", "ALeCaR2N", "ScanALeCaR"]
  #print(self.df_all)
            
  wb = Workbook() 

  # add_sheet is used to create sheet. 
  filename = our_algo + ' t-test results'
  sheet1 = wb.add_sheet(filename) 
  datasets = self.df["dataset"].unique()
  row=1
  writeHeader(sheet1, our_algo, "Other Algorithm")
  for other_algo in other_algos:
#     sheet1.write(row, 0, other_algo) 
#     row= row+1
    for datas in datasets:
        self.df_data= self.df[ self.df["dataset"] == datas]
        cache_sizes = self.df_data["cache_size"].unique()
        for cache_size in cache_sizes:
            self.df_cache = self.df_data[(self.df_data["cache_size"] == cache_size) ]
            
#             t_test_results.append(l)
            writeInCsv(sheet1,row, self.df_cache, our_algo, other_algo, datas, cache_size)
            row= row+1
            
#             sheet1.write(row, datas, cache_size, alecar_mean, alecar_std,scanalecar_mean, scanalecar_std,t2, p2) 
  
  wb.save(outputfile+"/"+our_algo+'_t-test results.xls')
  


  # In[47]:


  plt.figure()

  filenames = [self.infile]
  for filename in filenames:
    self.df = pd.read_excel(filename, keep_default_na=False, na_values=['#N/A'])
    trace_types = self.df["dataset"].unique()
#     trace_types = ['MSR','FIU', 'CloudVPS'] 
#     self.df_type = self.df[(self.df["type"] == trace_type) ]
    for trace_type in trace_types:
        self.df_type = self.df[(self.df["dataset"] == trace_type) ]
        cache_sizes = self.df_type["cache_size"].unique()
        for cache_size in cache_sizes:
            self.df_cache = self.df_type[(self.df["cache_size"] == cache_size) ]
            print("***** Trace: " + trace_type + " Cache size: " + str(cache_size*10) +"*******")
            
#             self.df_cache[['ARC', 'ALeCaRN','ScanALeCaR']].plot(kind='box')
            fig, ax = plt.subplots(figsize =(9, 7)) 
            sns.violinplot(ax = ax, data = self.df_cache.iloc[:, 4:12])
            plt.title(" Trace: " + trace_type + " Cache size: " + str(cache_size*10))
            plt.show()
           
   

