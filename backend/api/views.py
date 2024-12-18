from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .serializers import CategorySerializer, EventSerializer
from .models import Category, Event

@api_view(['GET'])
def get_events_and_push_to_db(request):
    api_url = 'https://eonet.gsfc.nasa.gov/api/v3/events'
    response = requests.get(api_url, verify=False)
    data = response.json()

    events = data.get('events', [])
    for event in events:
        # Salvar ou atualizar a categoria
        category_data = event['categories'][0] if event.get('categories') else None
        if category_data:
            category, created = Category.objects.get_or_create(
                id=category_data['id'],
                defaults={'name': category_data['title']}
            )
        else:
            category = None

        # Salvar ou atualizar o evento
        event_obj, created = Event.objects.update_or_create(
            id=event['id'],
            defaults={
                'title': event.get('title', ''),
                'description': event.get('description', ''),
                'date': event['geometry'][0]['date'] if event.get('geometry') else None,
                'link': event.get('link', ''),
                'category': category,
                # Salva todos os dados de geometry e sources no banco como JSON
                'geometry': event.get('geometry', []),  # Armazena a lista completa de geometrias
                'sources': event.get('sources', [])    # Armazena a lista completa de fontes
            }
        )

    return Response({"message": "Dados salvos com sucesso!"})

@api_view(['GET'])
def get_events(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    country = request.query_params.get('country')
    category = request.query_params.get('category')

    events = Event.objects.all()

# DJANGO FILTER
# PAGINATION DRF
# Class based views

    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)
    if country:
        events = events.filter(country=country)
    if category:
        events = events.filter(category__id=category)

    serialized_events = EventSerializer(events, many=True).data

    return Response(serialized_events)

@api_view(['GET'])
def get_events_by_id(request, event_id):
    events_filtered_by_id = Event.objects.filter(id=event_id)

    serialized_events_filtered_by_id = EventSerializer(events_filtered_by_id, many=True).data

    return Response(serialized_events_filtered_by_id)

@api_view(['GET'])
def get_categories(request):
    try:
        categories = Category.objects.all()
        
        if not categories.exists():
            return Response({"message": "No categories found"}, status=404)

        serialized_categories = CategorySerializer(categories, many=True).data
        
        if not serialized_categories:
            return Response({"message": "Error serializing categories"}, status=500)

        return Response(serialized_categories, status=200)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# @api_view(['GET'])
# def filter_events_by_date(request):
#     start_date = request.query_params.get('start_date')
#     end_date = request.query_params.get('end_date')

#     events_filtered_by_date = Event.objects.all()

#     if start_date and end_date:
#         events_filtered_by_date = events_filtered_by_date.filter(start_date__gte=start_date, start_date__lte=end_date)
#     elif start_date:
#         events_filtered_by_date = events_filtered_by_date.filter(start_date__gte=start_date)
#     elif end_date:
#         events_filtered_by_date = events_filtered_by_date.filter(start_date__lte=end_date)

#     serialized_events_filtered_by_date = EventSerializer(events_filtered_by_date, many=True).data

#     return Response(serialized_events_filtered_by_date)

# #A FAZER: GET EVENT BY COUNTRY
# @api_view(['GET'])
# def filter_event_by_country(request):
#     country = request.query_params.get('country')

#     events_filtered_by_country = Event.objects.filter(country=country)

#     serialized_events_filtered_by_country = EventSerializer(events_filtered_by_country, many=True).data

#     return Response(serialized_events_filtered_by_country)
# @api_view(['GET'])
# def get_events_by_id(request, event_id):
#     events_filtered_by_id = Event.objects.filter(id=event_id)

#     serialized_events_filtered_by_id = EventSerializer(events_filtered_by_id, many=True).data

#     return Response(serialized_events_filtered_by_id)

# @api_view(['GET'])
# def filter_events_by_date(request):
#     start_date = request.query_params.get('start_date')
#     end_date = request.query_params.get('end_date')

#     events_filtered_by_date = Event.objects.all()

#     if start_date and end_date:
#         events_filtered_by_date = events_filtered_by_date.filter(start_date__gte=start_date, start_date__lte=end_date)
#     elif start_date:
#         events_filtered_by_date = events_filtered_by_date.filter(start_date__gte=start_date)
#     elif end_date:
#         events_filtered_by_date = events_filtered_by_date.filter(start_date__lte=end_date)

#     serialized_events_filtered_by_date = EventSerializer(events_filtered_by_date, many=True).data

#     return Response(serialized_events_filtered_by_date)

# #A FAZER: GET EVENT BY COUNTRY
# @api_view(['GET'])
# def filter_event_by_country(request):
#     country = request.query_params.get('country')

#     events_filtered_by_country = Event.objects.filter(country=country)

#     serialized_events_filtered_by_country = EventSerializer(events_filtered_by_country, many=True).data

#     return Response(serialized_events_filtered_by_country)