
import json
import requests
import time

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from .models import Question
# Create your views here.


BASE_URL = "https://api.stackexchange.com/2.2/questions"


def get_stackoverflow_questions(query_param_string):
    """[summary]

    Args:
        query_param_string ([type]): [description]
    """
    get_url = BASE_URL + query_param_string
    print(get_url)
    try:
        response = requests.get(get_url)
    except Exception as inst:
        print("GET STACKOVERFLOW FAILED", inst)

    return response


class QuestionView(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        """[summary]

        Args:
            request ([type]): [description]
            format ([type], optional): [description]. Defaults to None.
        """
        sort_params = ["activity", "votes", "hot", "creation", "week", "month"]
        orders = ["asc", "desc"]
        query_param_string = "?"
        sort = self.request.query_params.get('sort', None)
        
        order = self.request.query_params.get('order', None)
        page = self.request.query_params.get('page', 1)
        pagesize = self.request.query_params.get('pagesize', 10)
        fromdate = self.request.query_params.get('fromdate', None)
        todate = self.request.query_params.get('todate', None)
        mindate = self.request.query_params.get('mindate', None)
        maxdate = self.request.query_params.get('maxdate', None)
        tagged = self.request.query_params.get('tagged', None)

        pattern = '%Y-%m-%d'
        if fromdate is not None:
            epocfrom = int(time.mktime(time.strptime(fromdate, pattern)))
            query_param_string += "&fromdate=" + str(epocfrom)
        if todate is not None:
            epocto = int(time.mktime(time.strptime(todate, pattern)))
            query_param_string += "&to=" + str(epocto)
        if mindate is not None:
            epocmin = int(time.mktime(time.strptime(mindate, pattern)))
            query_param_string += "&to=" + str(epocmin)
        if maxdate is not None:
            epocmax = int(time.mktime(time.strptime(maxdate, pattern)))
            query_param_string += "&to=" + str(epocmax)
        
        if sort != "":
            if sort not in sort_params:
                return Response(
                    {
                        "error" : 
                        "Sort Param provided is not matching: Available Values are {0}".format(sort_params)
                    },
                    status=status.HTTP_200_OK
                )

            query_param_string += "sort=" + sort
        if order != "":
            if order not in orders:
                return Response(
                    {
                        "error" : 
                        "Order Param provided is not matching: Available Values are {0}".format(orders),
                    },
                    status=status.HTTP_200_OK
                )
            query_param_string += "&order=" + order
        if page:
            query_param_string += "&page=" + str(page)
        if pagesize:
            query_param_string += "&pagesize=" + str(pagesize)
        if tagged:
            query_param_string += "&tagged=" + tagged

        query_param_string += "&site=stackoverflow"
        
        result = Question.objects.filter(querystring=query_param_string)        
        if result:
            return Response(
                result[0].data,
                status=status.HTTP_200_OK
            )    
        
        response = get_stackoverflow_questions(query_param_string)
        Question.objects.create(
            querystring=query_param_string,
            data=response.json()
        )
        return Response(
            response.json(),
            status=status.HTTP_200_OK
        )
