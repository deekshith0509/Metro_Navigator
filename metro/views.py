
# metro_navigation/metro/views.py
from django.shortcuts import render
from .models import Station
from .services import MetroService


def home(request):
    stations = Station.objects.all().order_by('name')

    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        mode = request.POST.get('mode', 'time')

        metro_service = MetroService()
        result, error = metro_service.find_path(source, destination, mode)

        # Visualize the metro map after finding the path
        visualization_path = metro_service.visualize_metro_map(source, destination, mode)

        if error:
            return render(request, 'metro/home.html', {
                'stations': stations,
                'error': error,
                'visualization_path': visualization_path
            })

        return render(request, 'metro/result.html', {
            'result': result,
            'stations': stations,
            'source': source,
            'destination': destination,
            'mode': mode,
            'visualization_path': visualization_path
        })

    return render(request, 'metro/home.html', {'stations': stations})
