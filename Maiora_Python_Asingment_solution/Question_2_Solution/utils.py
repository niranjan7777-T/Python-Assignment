from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework import status



class Common:

    @staticmethod
    def create_payload(status, message, error, data):
        payload = {
            "status": status,
            "message": message,
            "error": error,
            "data": data
        }
        return payload

    @staticmethod
    def save_jokes_to_db(jokes):
        processed_jokes = []  # List for storing processed joke dictionaries for response

        

        for joke in jokes:  # Iterate through the jokes
            
            for jok in joke['jokes']:
                

            # Extract data from the joke dictionary
                category = jok['category']
                
                joke_type = jok['type']

                # Handle 'single' type jokes
                if joke_type == 'single':
                    joke_text = jok['joke']
                    setup = None
                    delivery = None
                # Handle 'twopart' type jokes
                elif joke_type == 'twopart':
                    joke_text = None
                    setup = jok['setup']
                    delivery = jok['delivery']
                else:
                    joke_text = None
                    setup = None
                    delivery = None

                # Extract other fields
                nsfw = jok.get('flags', {}).get('nsfw', False)
                political = jok.get('flags', {}).get('political', False)
                sexist = jok.get('flags', {}).get('sexist', False)
                safe = jok['safe']
                lang = jok['lang']

                
                joke_data = {
                "category": category,
                "joke_type": joke_type,
                "setup": setup,
                "delivery": delivery,
                "joke_text": joke_text,
                "nsfw": nsfw,
                "political": political,
                "sexist": sexist,
                "safe": safe,
                "lang": lang,
            
                }

                serializer = JokeSerializer(data=joke_data)
                if serializer.is_valid():
                    joke_instance = serializer.save()  # Save to the database
                    processed_jokes.append(serializer.data)  # Add serialized data to the response
                else:
                    response_payload = Common.create_payload(False, "Error While Processing Data", str(e), None)
                    return JsonResponse(response_payload, status=status.HTTP_400_BAD_REQUEST)

                # Add to the response list as a dictionary
                processed_jokes.append({
                    "id": joke_instance.id,
                    "category": category,
                    "joke_type": joke_type,
                    "setup": setup,
                    "delivery": delivery,
                    "joke_text": joke_text,
                    "nsfw": nsfw,
                    "political": political,
                    "sexist": sexist,
                    "safe": safe,
                    "lang": lang,
                })

        return processed_jokes