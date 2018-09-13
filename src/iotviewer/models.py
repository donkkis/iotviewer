
class MultiSeriesResponse(object):
    """
    A set of VehicleResponse objects, presumably from a given time interval
    """
    def __init__(self):
        self.vehicles = []

class VehicleResponse(object):
    """
    A set of DatanodeSeries objects, presumably from a given time interval
    """
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.series = []

class DatanodeSeries(object):
    """
    A set of DatanodeResponse objects, presumably from a given time interval
    """    
    def __init__(self, datanode_id):
        self.datanode_id = datanode_id
        self.responses = []

class DatanodeResponse(object):
    """
    Represents a single response instance from a given vehicle/datanode pair 
    at a given time instant
    """
    
    def __init__(self, dtype, timestamp, value):
        self.dtype = dtype
        self.timestamp = timestamp
        self.value = value
        
class DatasetArray(object):
    """
    A collection of datasets that we will pass to displayseries.html as 
    JSONified string
    """
    
    def __init__(self, datasets=[]):
        self.datasets = datasets
        
    def serialize(self):
        ser = "["
        for dataset in self.datasets:
            ser = ser + dataset.serialize() + ","
        ser += "]"
        return ser
            
        
class Dataset(object):
    """
    A dataset instance to be passed to displayseries.html
    
    Args:
        label (string) : Vehicle/asset name of the series to be plotted
        borderColor (string) : HTML color code used in plotting of the series
    """
    
    def __init__(self, label, data=[]):
        self.data = data
        self.label = label
        self.borderColor = "#3e95cd"
        self.fill = False
        self.showLine = True

    def __str__(self):
        s = ""
        for i in range(len(self.data)):
            s = s + str(self.data[i].x) + ", " + str(self.data[i].y) + "\n"
        return s
    
    def serialize(self):
        dataset_json = "{data: ["
        for datum in self.data:
            dataset_json = dataset_json + datum.serialize() + ","
        dataset_json += "], "
        dataset_json += f"label: '{self.label}', borderColor: '{self.borderColor}', fill: {str(self.fill).lower()}, showLine: {str(self.showLine).lower()}}}"
        return dataset_json
    
class DataPoint(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def serialize(self):
        return "{{x : {}, y : {} }}".format(self.x, self.y)
