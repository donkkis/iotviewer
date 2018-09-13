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
import pandas as pd
from .models import Dataset
from .models import DataPoint
from .models import DatasetArray

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
        dataset_arr.datasets = [] should not be needed! For some reason datasets
        are persisted between consecutive calls
    """
    if request.method == 'POST':
        
        print(request.POST.keys())
        
        interval = [str.strip(dt) for dt in request.POST.getlist('datefilter')[0].split('-')]
        vehicles = request.POST.getlist('vehicleSelect')
        dnodes = request.POST.getlist('datanodeSelect')
        
        print(interval)
        print(vehicles)
        print(dnodes)
        
        if len(vehicles) == 0 or len(dnodes) == 0:
            #empty request should not be allowed but we double check here
            raise Exception("No arguments given")
        
        elif interval[0] and interval[1]:
            #some datetimerange given
            print('daterange given')
            start = interval[0]
            stop = interval[1]
            res_list = get_data_from_selected(vehicles, dnodes, start, stop)
            
            #implement data unpacking
            #need separate models.Dataset instance for each (veh_id, dnode_id)
            dataset_arr = DatasetArray()
            dataset_arr.datasets = []
            
            for veh_id, veh_response in res_list.items():
                for dnode_id, dnode_series in veh_response.items():
                    dataset = Dataset(label=f"{veh_id}_{dnode_id}")                    
                    for dnode_response in dnode_series:
                        x = dnode_response['ts']
                        y = dnode_response['v']
                        #print(veh_id, dnode_id, dnode_response['ts'], dnode_response['v'])
                        dataset.data.append(DataPoint(x, y))
                    #print(dataset)
                    dataset_arr.datasets.append(dataset)
                
            context = {
                    'datasets' : dataset_arr.serialize(),
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
    
