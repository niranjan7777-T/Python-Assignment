# views.py

import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import *
import json
from .utils import *
from Question_1_Solution import settings
import pandas as pd




class JokeAPI(APIView):
    def post(self, request):
        
        try:
            jokes_from_api = []

            total_jokes = 100
            jokes_per_request = 10
            
            amount = total_jokes // jokes_per_request

            # Loop to make requests and accumulate jokes
            for i in range(amount):  # Loop until we get the required number of jokes
                url = f"{os.environ.get('JOKE_API')}" + '?amount=' + f"{amount}"
                response = requests.get(url)

                if response.status_code == 200:
                    joke_data = response.json()
                    jokes_from_api.append(joke_data)
            
            

            # Save jokes and get processed data for response
            processed_jokes = Common.save_jokes_to_db(jokes_from_api)

            # Prepare and return the response
            payload = {
                "status": True,
                "Message": "Jokes Fetched and Stored Successfully",
                "data": processed_jokes,
                "error": None
                
            }
            payload = Common.create_payload(True,"Jokes Fetched and Stored Successfully",None,processed_jokes)
            return JsonResponse(payload, status=status.HTTP_200_OK)

        except Exception as e:
            response_payload = Common.create_payload(False, "Error While Processing Data", str(e), None)
            return JsonResponse(response_payload, status=status.HTTP_400_BAD_REQUEST)

class UploadExcel(APIView):

    def post(self, request):
        try:
            uploaded_file = request.FILES['excel']

            # Ensure the media directory exists
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # Save the uploaded file temporarily
            temp_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(temp_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            # Read the Excel file using pandas
            df = pd.read_excel(temp_path)

            # Convert to CSV
            csv_file_name = f"{os.path.splitext(uploaded_file.name)[0]}.csv"
            static_csv_path = os.path.join(settings.MEDIA_ROOT, 'uploads', csv_file_name)

            # Ensure the target directory exists
            os.makedirs(os.path.dirname(static_csv_path), exist_ok=True)

            # Save as CSV in the static folder
            df.to_csv(static_csv_path, index=False)

            # Optionally, delete the temporary file
            os.remove(temp_path)

            return Response({
                "status": "success",
                "message": f"File saved as CSV at {static_csv_path}"
            })

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=400)






       


