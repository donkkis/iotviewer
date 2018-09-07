
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