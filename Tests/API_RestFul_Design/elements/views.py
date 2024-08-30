from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Element
from .serializer import ElementSerializer
import logging

logger = logging.getLogger('django')
logger.addHandler('file')


#Function to parse the data from the request
def parse_data(data):
    new_data = dict()

    new_data['id'] = data['id']
    new_data['device_name'] = data['deviceName']
    element_data = data['data']

    #Transforming the data in the element to an array of integers
    element_data = [[int(num) for num in line.split() ] for line in element_data]
    element_data = [num for line in element_data for num in line]

    #Normalizing the data in the element
    element_max_value = max(element_data)
    element_data_normalized = [round(num / element_max_value, 4) for num in element_data]
        
    #Calculating the average of the data before and after normalization
    element_data_average = sum(element_data) / len(element_data)
    element_data_normalized_average = sum(element_data_normalized) / len(element_data_normalized)

    new_data['average_before_normalization'] = element_data_average
    new_data['average_after_normalization'] = element_data_normalized_average
    new_data['data_size'] = len(element_data)
    new_data['raw_data'] = data

    return new_data


@csrf_exempt
def element_list(request):
    
    try:
        #Logging the request
        logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")

        if request.method == 'GET':
            elements = Element.objects.all()
            serializer = ElementSerializer(elements, many=True)

            #Logging the response
            logger.info(f"Response data: {serializer.data}")
            return JsonResponse(serializer.data, safe=False)
        
        elif request.method == 'POST':
            data = JSONParser().parse(request)

            new_data = parse_data(data)
          
            serializer = ElementSerializer(data=new_data)

            #Validating the data and saving the new element
            if serializer.is_valid():
                serializer.save()

                #Logging the response
                logger.info(f"New Element created, Response data: {serializer.data}")
                return JsonResponse(serializer.data, status=201)
            
            #Logging the validation error if the data is not valid and returning the error
            logger.error(f"Validation error: {serializer.errors}")
            return HttpResponse(serializer.errors, status=400)
        
    #Loggin any error that occurs during the request
    except Exception as e:
        logger.error(f"Error: {e}")
        return JsonResponse(status=400, content=e)
    
    
@csrf_exempt
def element_detail(request, pk):
 
    #Logging the request
    logger.info(f"Request method: {request.method}, Request path: {request.path}, Request body: {request.body}")
    try:
        #Getting the element with the id provided
        element = Element.objects.get(pk=pk)
    

        
        if request.method == 'GET':
            
            #Serializing the element and returning the data
            serializer = ElementSerializer(element)
            logger.info(f"Response data: {serializer.data}")
            return JsonResponse(serializer.data)



        elif request.method == 'PUT':
            #Parsing the data from the request to update the element
            data = JSONParser().parse(request)

            #Validating that the data is not empty
            if len(data) == 0:
                logger.error(f"No data provided for update")
                return JsonResponse(status=400, data={"error": "No data provided for update"})

  
            
            #Parsing the data to update the element
            data['id'] = pk
            data['average_before_normalization'] = element.average_before_normalization
            data['average_after_normalization'] = element.average_after_normalization
            data['data_size'] = element.data_size
            data['raw_data'] = element.raw_data

            
          
           #Serializing the data to update the element
            serializer = ElementSerializer(element, data=data)
            
            #Validating the data and saving the updated element
            if serializer.is_valid():
                serializer.save()

                #Logging the response
                logger.info(f"Element updated with id={pk}, Response data: {serializer.data}")
                return JsonResponse(serializer.data)
            
            #Logging the validation error if the data is not valid and returning the error
            logger.error(f"Validation error: {serializer.errors}")
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            
            #Deleting the element
            element.delete()
            logger.info(f"Element deleted with id={pk}")
            return HttpResponse(status=204)
        

    #Logging the error if the element is not found
    except Element.DoesNotExist:
        logger.error(f"Element with id={pk} not found")
        response = JsonResponse(status=404, data={"error": "Element not found"})
        logger.error(f"Response: {response.content}")
        return response
    
    #Logging any error that occurs during the request
    except Exception as e:
        logger.error(f"Error: {e}")
        return JsonResponse(status=400, content=e)

        
    