from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()

class HomeView(View):   #use context in html js tags
	def get(self, request, *args, **kwargs):
		data = {"customers": User.objects.all().count(),} #can use database info as the data
		context = {'data':data}
		return render(request, 'charts.html', context)

# def get_data(request, *args, **kwargs): #data is url, js on page finds it there
# 	data = {
# 		"sales": 100,
# 		"customers": 10,
# 	}
# 	return JsonResponse(data) # http response

class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		qs_count = User.objects.all().count()
		labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]  #x values
		default_items = [qs_count, 23, 2, 3, 12, 2]							#y values
		colour_background = [
			'rgba(255, 99, 132, 0.2)',
			'rgba(54, 162, 235, 0.2)',
			'rgba(255, 206, 86, 0.2)',
			'rgba(75, 192, 192, 0.2)',
			'rgba(153, 102, 255, 0.2)',
			'rgba(255, 159, 64, 0.2)'
		]
		colour_border = [
			'rgba(255,99,232,100)',
			'rgba(54, 162, 235, 1)',
			'rgba(255, 206, 86, 1)',
			'rgba(75, 192, 192, 1)',
			'rgba(153, 102, 255, 1)',
			'rgba(255, 159, 64, 1)'
		]
		data = {
				"labels": labels,				#API veiw, data json object, access by data.key
				"default": default_items,
				"colour_background": colour_background,
				"colour_border": colour_border,
		}
		return Response(data)

class ChartViewTwo(View):   #use context in html js tags
	def get(self, request, *args, **kwargs):
		return render(request, 'charts2.html', context)

class ChartDataTwo(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		qs_count = User.objects.all().count()
		labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
		default_items = [qs_count, 23, 2, 3, 12, 2]
		data = {
				"labels": labels,
				"default": default_items,
		}
		return Response(data)