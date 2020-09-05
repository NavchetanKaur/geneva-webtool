from django.shortcuts import render
from django.http import HttpResponse
import gene_expression
from gene_expression import gene_exp_table, gse_description
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np
import io
import urllib, base64
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Bar
from plotly.graph_objs import Scatter
import plotly.express as px
# Create your views here.




def geneva_home(request):
	return render(request, 'geneva_app/home.html')


def gene_table(request):
    uinput = request.GET['gene_name']
    uinput = uinput.strip() 
    output = gene_exp_table(uinput)[1]
    gse_list = output['GSE'].to_list()
    gse_title = output['GSE_title'].to_list()
    geneva_score = output['GENEVA'].to_list()
    geneva_score = [round(num, 2) for num in geneva_score]

    return render(request, 'geneva_app/gene_table.html', {'zipped_list': zip(gse_list, gse_title, geneva_score), 'gene_entry': uinput})   
    

    
def gse_elab(request):
	uinput_1 = request.GET['gene_name']
	uinput_1 = uinput_1.strip()
	uinput_2 = request.GET['gse_id']
	uinput_2 = uinput_2.strip()
	output = gse_description(uinput_1, uinput_2)
	gse_id = output[0]
	title = output[1]
	summary = output[2]
	link = output[3]
	plot_df_sm = output[4]
	plot_df = output[5]
	
	gene = uinput_1 


	df_col1 = plot_df_sm["GSM"].to_list()
	df_col2 = plot_df_sm["source"].to_list()
	df_col3 = plot_df_sm["title"].to_list()
	df_col4 = plot_df_sm["feature"].to_list()
	df_col5 = plot_df_sm[uinput_1].to_list()

	
	#BarPlot with plotly
	plot_div = plot([Bar(y=plot_df_sm['title'], x=plot_df_sm[uinput_1], orientation='h')], output_type='div')
	#plot_div = px.bar(plot_df_sm, x=plot_df_sm['title'], y=plot_df_sm[gene], hover_data=['GSM', 'source', 'title', 'feature'])

	#Scatter Plot
	plot2 = plot([Scatter(x = plot_df['meta1'], y = plot_df['meta2'], text=plot_df['title'], mode = 'markers+text',  textposition='top center',
		marker=dict(color=plot_df[gene], size=12, colorscale='Bluered', showscale=True), 
		textfont=dict(color='black', size=14, family='Times New Roman'))],output_type='div')
			


	return render(request, 'geneva_app/gse_description.html', {
		'gse_id': gse_id, 'title': title, 'summary': summary, 'link': link, 'gene_name': gene, 'plot1': plot_div, 'plot2': plot2,
		'zipped_list': zip(df_col1, df_col2, df_col3, df_col4, df_col5)})


    