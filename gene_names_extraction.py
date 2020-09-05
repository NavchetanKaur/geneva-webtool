#! usr/bin/python



import re
import pandas as pd


df = pd.read_csv('df_var.csv')

gene_list = list(df.columns) 


with open('gene_list.txt', 'w') as filehandle:
filehandle.writelines("%s\n" % gene for gene in gene_list)'''