from django.http import HttpResponse
from django.shortcuts import render
from .utils import get_available_datanodes
from .utils import get_available_vehicles
from .utils import get_data_from_selected
from django.http import HttpResponseForbidden
from .models import MultiSeriesResponse
from .models import VehicleResponse
from .models import DatanodeSeries
from .models import DatanodeResponse

def home(request):
    """
    display landing page. get available dnodes/vehicles and pass them to view
    """
    available_vehicles = get_available_vehicles()
    available_datanodes = get_available_datanodes()
    
    context = {
            'available_vehicles' : available_vehicles,
            'available_datanodes' : available_datanodes
            }
    
    return render(request, "iotviewer/landing.html", context)

def display(request):
    """
    get static data for given vehicles and dnodes
    POST request should include these variables
    
    TODO:
        refactor to use request variables and not static methods
    
    """
    if request.method == 'POST':
        
        print(request.POST.keys())
        
        interval = [str.strip(dt) for dt in request.POST.getlist('datefilter')[0].split('-')]
        vehicles = request.POST.getlist('vehicleSelect')
        dnodes = request.POST.getlist('datanodeSelect')
        
        print(interval)
        
        if len(vehicles) == 0 or len(dnodes) == 0:
            #empty request should not be allowed but this acts as a double 
            #check
            raise Exception("No arguments given")
        
        elif interval[0] and interval[1]:
            #some datetimerange given
            print('daterange given')
            start = interval[0]
            stop = interval[1]
            res_list = get_data_from_selected(vehicles, dnodes, start, stop)
                
            context = {
                    'res_list' : res_list
                    }
            return render(request, 'iotviewer/displayseries.html', context)
            
        else:
            #handle case where no datetimerange is given; render a table 
            #of most recent values            
            res_list = get_data_from_selected(vehicles, dnodes)            
            context = {
                    'res_list' : res_list
                    }                                
            return render(request, 'iotviewer/display.html', context)
    else:
        return HttpResponseForbidden()
    
def display_series(request):
    
    if request.method == 'POST':
        return HttpResponse('test')
    
    else:
        return HttpResponseForbidden()
    
