from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
import numpy as np
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from django.views.generic import TemplateView
import json
from django.core import serializers
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser,MultiPartParser,FormParser
import os


# class Graph(TemplateView):
#     template_name = 'graph.html'

#     def get_context_data(self, **kwargs):
#         context = super(Graph, self).get_context_data(**kwargs)

#         x = [-2,0,4,6,7]
#         y = [q**2-q+3 for q in x]
#         trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
#                             mode="lines",  name='1st Trace')

#         data=go.Data([trace1])
#         layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})
#         figure=go.Figure(data=data,layout=layout)
#         div = opy.plot(figure, auto_open=False, output_type='div')

#         context['graph'] = div

#         return context


def getSum(n):
	sum = 0
	n = int(n)
	while(n!=0):
		sum = sum+n%10
		n=n/10
	return(sum)

def writeGraph(cabinName):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	a = os.path.join(BASE_DIR, '2018_02_10_Data_Scraping_Output.xlsx')
	scrapeWB = pd.ExcelFile(a)
	df = pd.DataFrame()
	SheetNames = scrapeWB.sheet_names
	for Name in SheetNames:
		mysheet = scrapeWB.parse(Name) #dataframe
		if (mysheet.empty):
			print("WARNING: Empty data", Name, len(mysheet))
		else:
			mysheet = mysheet[pd.notnull(mysheet["CabinName"])]
			mysheet.reset_index(drop=True, inplace=True)
			c = Name.encode('utf-8')
			# mysheet['CabinName'] = mysheet['CabinName'].apply(lambda x: x.encode('utf-8'))
			# for i in range(0,len(mysheet['CabinName'])):
			# 	print mysheet['CabinName'][i]
			# 	if (isinstance(mysheet['CabinName'][i], str)):
			# 		mysheet['CabinName'][i] = str(mysheet['CabinName'][i])
			# 	elif(isinstance(mysheet['CabinName'][i], int)):
			# 		mysheet['CabinName'][i] = str(mysheet['CabinName'][i])
			# 	elif(isinstance(mysheet['CabinName'][i], unicode)):
			# 		mysheet['CabinName'][i] = mysheet['CabinName'][i].encode('utf-8')
			# 	else:
			# 		mysheet = mysheet.drop(mysheet.index[[i]])

			mysheet['CabinName2'] = c + '-' + mysheet['CabinName'].astype(str)
			df = df.append(mysheet, ignore_index=True)
	# df.to_csv('out.csv', encoding='utf-8')
	df = df.loc[df['CabinName'] == cabinName]
	df = df.reset_index(drop=True)
	# print df
	df2 = pd.DataFrame()
	df2['months'] = ['monthAvailabe_1','monthAvailabe_2','monthAvailabe_3','monthAvailabe_4','monthAvailabe_5','monthAvailabe_6','monthAvailabe_7']
	df2['value'] = [0,0,0,0,0,0,0]
	traces = []
	for i in range(0,len(df['CabinName2'])):
		for j in range(0,len(df2)):
			z = df['monthAvailabe_'+str(j+1)][i].split('\'')
			sum = getSum(z[1])
			df2['value'][j] = 30 - sum
			# print df['monthAvailabe_'+str(t)][i]
		# print df2
		c = go.Scatter(
			x = list(df2['months'].values),
			y = list(df2['value'].values),
			mode = 'lines+markers',
			name = str(df['CabinName2'][i])
		)
		traces.append(c)
		# print traces
	return(traces)

def home(request):
	data=go.Data(writeGraph('The View'))
	layout=go.Layout(title="The View", xaxis={'title':'Months'}, yaxis={'title':'No. of Days Available'})
	figure=go.Figure(data=data,layout=layout)
	config={'showLink': False,
			'displayModeBar': False
		# 'modeBarButtonsToRemove':  ['sendDataToCloud']
	}
	# cntxt = opy.plot(figure, auto_open=False, output_type='div')
	cntxt = opy.plot(figure, include_plotlyjs=False, output_type='div', config=config)
	cntxt = {
		'cntxt':cntxt,
	}
	return render(request, 'index.html', cntxt)

@api_view(['GET'])
def graph(request):
	cabinName = request.GET.get('cabinName')
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	a = os.path.join(BASE_DIR, '2018_02_10_Data_Scraping_Output.xlsx')
	scrapeWB = pd.ExcelFile(a)
	df = pd.DataFrame()
	SheetNames = scrapeWB.sheet_names
	for Name in SheetNames:
		mysheet = scrapeWB.parse(Name) #dataframe
		if (mysheet.empty):
			print("WARNING: Empty data", Name, len(mysheet))
		else:
			mysheet = mysheet[pd.notnull(mysheet["CabinName"])]
			mysheet.reset_index(drop=True, inplace=True)
			c = Name.encode('utf-8')
			mysheet['CabinName2'] = c + '-' + mysheet['CabinName'].astype(str)
			df = df.append(mysheet, ignore_index=True)
	# df.to_csv('out.csv', encoding='utf-8')
	df = df.loc[df['CabinName'] == cabinName]
	df = df.reset_index(drop=True)
	# print df
	df2 = pd.DataFrame()
	df2['months'] = ['monthAvailabe_1','monthAvailabe_2','monthAvailabe_3','monthAvailabe_4','monthAvailabe_5','monthAvailabe_6','monthAvailabe_7']
	df2['value'] = [0,0,0,0,0,0,0]
	traces = []
	for i in range(0,len(df['CabinName2'])):
		for j in range(0,len(df2)):
			z = df['monthAvailabe_'+str(j+1)][i].split('\'')
			sum = getSum(z[1])
			df2['value'][j] = 30 - sum
			# print df['monthAvailabe_'+str(t)][i]
		# print df2
		c = go.Scatter(
			x = list(df2['months'].values),
			y = list(df2['value'].values),
			mode = 'lines+markers',
			name = str(df['CabinName2'][i])
		)
		traces.append(c)
		# print traces
	data=go.Data(traces)
	layout=go.Layout(title=cabinName, xaxis={'title':'Months'}, yaxis={'title':'No. of Days Available'})
	figure=go.Figure(data=data,layout=layout)
	config={'showLink': False,
			'displayModeBar': False
		# 'modeBarButtonsToRemove':  ['sendDataToCloud']
	}
	# cntxt = opy.plot(figure, auto_open=False, output_type='div')
	cntxt = opy.plot(figure, include_plotlyjs=False, output_type='div', config=config)
	# cntxt = serializers.serialize('json',cntxt)
	return Response({"cntxt":cntxt})
