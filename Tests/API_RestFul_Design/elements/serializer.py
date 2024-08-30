from rest_framework import serializers
from .models import Element


#Serializer for the Element model
class ElementSerializer(serializers.ModelSerializer):


  #Method to indicate the model to be used and the fields to be serialized
  class Meta:
    model = Element
    fields = '__all__'
