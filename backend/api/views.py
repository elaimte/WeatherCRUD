
import requests
from django.conf import settings
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .tokens import CustomRefreshToken
from .models import UserCollection, UserSearchHistory
from .serializers import UserRegistrationSerializer, UserLoginSerializer, SearchHistorySerializer
from django.http import JsonResponse

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = CustomRefreshToken.for_user(user)
            return Response({"message": "Login successful","refresh":str(refresh),"access":str(refresh['access_token'])} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = UserCollection.objects(email=email).first()
            if user and user.check_password(password):
                refresh = CustomRefreshToken.for_user(user)
                return Response({"message": "Login successful","refresh":str(refresh),"access":str(refresh['access_token'])}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WeatherView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, city_name):
        user_id = str(request.user.id)
        user_search_history = UserSearchHistory.objects(user_id=user_id).first()
        if user_search_history is None:
            user_search_history = UserSearchHistory(user_id=user_id)
            user_search_history.save()
        base_url = "http://dataservice.accuweather.com/"
        api_key = settings.ACCUWEATHER_API_KEY

        # Step 1: Find the location key for the city
        location_search_url = f"{base_url}/locations/v1/cities/search"
        search_params = {"apikey": api_key, "q": city_name}
        location_response = requests.get(location_search_url, params=search_params)        
        if location_response.status_code != 200:
            user_search_history.add_search_history(city_name,"Error Fetching Data from Source")
            return Response({"message": "Error fetching Data from Source"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location_data = location_response.json()[0]
            location_key = location_data['Key']
        except:
            user_search_history.add_search_history(city_name,"Error Fetching location data")
            return Response({"message": "Error fetching location data"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Use the location key to get weather data
        weather_url = f"{base_url}/currentconditions/v1/{location_key}"
        weather_params = {"apikey": api_key}
        weather_response = requests.get(weather_url, params=weather_params)

        if weather_response.status_code != 200:
            user_search_history.add_search_history(city_name,"Failed to fetch weather data")
            return Response({"message": "Error fetching weather data"}, status=status.HTTP_400_BAD_REQUEST)
        weather_data = weather_response.json()
        weather_data_for_db = "{}° C".format(weather_data[0]['Temperature']['Metric']['Value'])
        user_search_history.add_search_history(city_name,weather_data_for_db)
        return Response(weather_data[0]['Temperature'], status=status.HTTP_200_OK)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user_id = str(request.user.id)
        user_search_history = UserSearchHistory.objects(user_id=user_id).first()
        if user_search_history:
            serializer = SearchHistorySerializer(user_search_history.search_history, many=True)
            return Response(serializer.data)
        else:
            return Response([])


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request,'dashboard.html')


def autocomplete_city(request):
    query = request.GET.get('q', '')
    api_key = settings.ACCUWEATHER_API_KEY
    url = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={api_key}&q={query}"

    response = requests.get(url)
    return JsonResponse(response.json(), safe=False)