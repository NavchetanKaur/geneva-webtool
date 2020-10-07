import pandas as pd
import datatable as dt
from sklearn import linear_model
from multiprocessing import Pool, set_start_method
import numpy as np




obj1 = ['df_embed','df_meta','df_var_mean','exp','gse_meta',"df_N"] 
data_dict = {}
for o1 in obj1:
    fn = (o1+".csv")
    data_dict[o1]=dt.fread(fn).to_pandas()

# dict of data frames
    
data_dict["exp"] = data_dict["exp"].set_index("ID")
data_dict["exp"] = data_dict["exp"].astype(np.uint8)


total_GSE = 500


## function defining linear regression

def f1(df1):
    x1 = df1[['meta1','meta2']].values
    y1 = df1['gene'].values
    clf = linear_model.LinearRegression()
    clf.fit(x1,y1)
    df1 = df1 = pd.DataFrame({"GSE":[df1['GSE'].values[0]],'r2':[clf.score(x1,y1)]})
    return(df1)


def query_exp(query_expr):
	query_expr = query_expr.merge(data_dict['df_meta'][["GSM","GSE"]],how="inner", on="GSM")
	df_gene = query_expr.groupby('GSE', as_index=False)["gene"].var()
	df_gene.rename(columns = {'gene':'total_var'}, inplace = True)
	df_N_sub = data_dict["df_N"][(data_dict["df_N"]["GSE_N"]<=20) & (data_dict["df_N"]["GSE_N"]>=6)]
	df_gene = df_gene.merge(df_N_sub,how="inner", on="GSE")
	df_gene = df_gene.merge(data_dict["df_var_mean"],how="inner", on="GSE")
	df_gene['GENEVA'] = df_gene["total_var"]/df_gene["var_mean"]
	df_gene = df_gene.sort_values("GENEVA",ascending=False)
	df_gene = df_gene.iloc[0:total_GSE,]
	
	df_cor = query_expr
	df_cor= df_cor.merge(data_dict["df_embed"],how="inner", on=["GSM","GSE"])
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


	return query_expr, df_gene, df1


def gene_exp_table(gene):
	query_expr = pd.DataFrame({"GSM":data_dict["exp"].columns,"gene":data_dict["exp"].loc[gene,]})
	output = query_exp(query_expr)
	df_gene = output[1]
	df1 = output[2]
	
	return df_gene, df1

def multi_genes_set_table(up_gene, dn_gene):  

	if not dn_gene:
		up_expr = data_dict["exp"].loc[up_gene,]
		up_expr = up_expr.mean(axis=0)
		query_expr = pd.DataFrame({"GSM":up_expr.index,"gene":up_expr })

	else:
		up_expr = data_dict["exp"].loc[up_gene,]
		up_expr = up_expr.mean(axis=0)
		dn_expr = data_dict["exp"].loc[dn_gene,]
		dn_expr = dn_expr.mean(axis=0)

		query_expr = up_expr-dn_expr
		query_expr = pd.DataFrame({"GSM":query_expr.index,"gene":query_expr })

	output = query_exp(query_expr)
	query_exprm = output[0]
	df_gene = output[1]
	df1 = output[2]
	
	return query_exprm, df_gene, df1

	

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

def gene_signature_gse_description(up_gene, dn_gene, gse_id):
	
	query_expr = multi_genes_set_table(up_gene, dn_gene)[0]
	df_gene = multi_genes_set_table(up_gene, dn_gene)[1]
	
	plot_df = data_dict['df_meta'][data_dict['df_meta']['GSE']==gse_id]
	plot_df = plot_df.merge(data_dict['df_embed'],on=["GSM",'GSE'],how="inner")
	plot_df = plot_df.merge(query_expr,how="inner", on=["GSM","GSE"])
	plot_df.rename(columns={"gene": "expression"},inplace = True)

	plot_df['meta1']=(plot_df['meta1']-plot_df['meta1'].mean())/plot_df['meta1'].std()
	plot_df['meta2']=(plot_df['meta2']-plot_df['meta2'].mean())/plot_df['meta2'].std()
	plot_df['meta2']=plot_df['meta2'] + np.random.normal(0, 0.1, len(plot_df['meta2']))

	plot_df['len']=plot_df['title'].str.len()
	plot_df=plot_df.sort_values("expression",ascending=True)

	
	df_gene_index = df_gene.set_index("GSE")
	title = df_gene_index['GSE_title'][gse_id]
	summary = df_gene_index['GSE_summary'][gse_id]
	gse_link = df_gene_index['GSE_link'][gse_id]

	plot_df_sm=plot_df[['GSM','source','title','feature',"expression"]]
	plot_df_sm.rename(columns={"feature": "characteristics"}, inplace = True)

	return  gse_id, title, summary, gse_link, plot_df_sm, plot_df
