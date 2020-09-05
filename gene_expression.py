import pandas as pd
import datatable as dt
from sklearn import linear_model
from multiprocessing import Pool, set_start_method
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import io
import urllib, base64



obj1 = ['df_embed','df_meta','df_var','df_var_mean','exp','gse_meta',"df_N"]
data_dict = {}
for o1 in obj1:
    fn = (o1+".csv")
    data_dict[o1]=dt.fread(fn).to_pandas()

# dict of data frames
    
data_dict["exp"] = data_dict["exp"].set_index("ID")


total_GSE = 500


## function defining linear regression

def f1(df1):
    x1 = df1[['meta1','meta2']].values
    y1 = df1['gene'].values
    clf = linear_model.LinearRegression()
    clf.fit(x1,y1)
    df1 = df1 = pd.DataFrame({"GSE":[df1['GSE'].values[0]],'r2':[clf.score(x1,y1)]})
    return(df1)




def gene_exp_table(gene):
	df_gene = pd.DataFrame({})
	df_gene["GSE"]=data_dict["df_var"]["GSE"]
	df_gene["total_var"]=data_dict["df_var"][gene]
	df_N_sub = data_dict["df_N"][(data_dict["df_N"]["GSE_N"]<=20) & (data_dict["df_N"]["GSE_N"]>=6)]
	df_gene = df_gene.merge(df_N_sub,how="inner", on="GSE")
	df_gene = df_gene.merge(data_dict["df_var_mean"],how="inner", on="GSE")
	df_gene['GENEVA'] = df_gene["total_var"]/df_gene["var_mean"]
	df_gene = df_gene.sort_values("GENEVA",ascending=False)
	df_gene = df_gene.iloc[0:total_GSE,]


	df_cor = pd.DataFrame({"GSM":data_dict["exp"].columns,"gene":data_dict["exp"].loc[gene,]})
	df_cor= df_cor.merge(data_dict["df_embed"],how="inner", on="GSM")
	df_cor = df_cor[df_cor["GSE"].isin(df_gene["GSE"])].groupby("GSE")

	dflist = [f1(group) for name, group in df_cor]
	df_cor = pd.concat(dflist)


	df_gene = df_gene.merge(df_cor,how="inner",on="GSE")



	df_gene['GENEVA'] = df_gene['total_var']/df_gene['var_mean']*df_gene['r2']
	df_gene = df_gene.merge(data_dict['gse_meta'], left_on="GSE", right_on="GSE_id")



	l1 = np.where(~df_gene.columns.str.contains("ID|id|V1"))[0]
	df_gene=df_gene.iloc[:,l1]
	df_gene=df_gene.sort_values("GENEVA",ascending=False)

	df1 = df_gene[['GSE','GSE_title','GENEVA']]

	return df_gene, df1



def gse_description(gene, gse_id):
	np.random.seed(seed=363)
	plot_df = data_dict['df_meta'][data_dict['df_meta']['GSE']==gse_id]
	plot_df = plot_df.merge(data_dict['df_embed'],on=["GSM",'GSE'],how="inner")
	plot_df[gene]= data_dict["exp"].loc[gene,plot_df['GSM']].values

	plot_df['meta1']=(plot_df['meta1']-plot_df['meta1'].mean())/plot_df['meta1'].std()

	plot_df['meta2']=(plot_df['meta2']-plot_df['meta2'].mean())/plot_df['meta2'].std()
	plot_df['meta2']=plot_df['meta2'] + np.random.normal(0, 0.1, len(plot_df['meta2']))

	plot_df['len']=plot_df['title'].str.len()
	plot_df=plot_df.sort_values(gene,ascending=True)

	# 1. show GSE information
	df_gene = gene_exp_table(gene)[0]
	df_gene_index = df_gene.set_index("GSE")
	title = df_gene_index['GSE_title'][gse_id]
	summary = df_gene_index['GSE_summary'][gse_id]
	gse_link = df_gene_index['GSE_link'][gse_id]

	# 2. display GSM data
	plot_df_sm=plot_df[['GSM','source','title','feature',gene]]
	plot_df_sm.rename(columns={"feature": "characteristics"})
	

	return gse_id, title, summary, gse_link, plot_df_sm, plot_df

