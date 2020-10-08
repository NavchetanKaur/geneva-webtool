from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

import gene_expression
from gene_expression import gene_exp_table

from . import serializers
from rest_framework_swagger.views import get_swagger_view



class GeneApiView(generics.GenericAPIView):
    """Returns Gene variance expression table for an gene"""
    serializer_class = serializers.GeneSerializer
    permission_classes = [AllowAny,]
        #def get(self, response, format=None):
        #obj = ["UNOS antigen mapping for WHO HLA alleles"]
        #return Response({'Web Services': obj})

    def post(self, request, format=None):
        """Returns UNOS antigen for an allele.Enter IPD-IMGT/HLA allele fully resolved or upto second field with expression characters. The results yield UNOS antigen equivalency and Bw4/6 epitope. """
        """parameters:
            allele:string
            """
        serializer = serializers.GeneSerializer(data=request.data)    

        if serializer.is_valid(raise_exception=True):
            gene = serializer.data.get('gene')
            table = gene_expression.gene_exp_table(gene)[1]
            result = {'Expression Table': table}
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Check if it's a valid allele"}, status=status.HTTP_400_BAD_REQUEST)
                #serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
