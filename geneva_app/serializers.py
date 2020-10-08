from rest_framework import serializers


class GeneSerializer(serializers.Serializer):
	
	"""Create and return a new instance, given the validated data
	Serializes a name field for testing our APIView."""
	gene = serializers.CharField(max_length=None)
	


class GeneSetSerializer(serializers.Serializer):
	"""Serializes a name field for testing our APIView."""
	upregulated_genes = serializers.CharField(max_length=None)
	downregulated_genes = serializers.CharField(max_length=None) 