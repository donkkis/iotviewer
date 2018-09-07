import pandas as pd
from . import wrmclient

cl = wrmclient.Wrmclient()

def get_data_from_selected(vehicles, dnodes, start=None, stop=None):
    """
    Retrieve data from IOT Ticket API
    
    Args:
        vehicles (list(string)) : List of vehicleID:s
        dnodes (list(string)) : List of dnode cleartext names
    
    Returns:
        res_list (dict string->dict) : A dictionary that maps a vehicleID to 
            response from the selected dnodes from that vehicleID
    """
    res_list = {}
    
    try:
        for vehicle in vehicles:
            res_list[vehicle] = {}
            for dnode in dnodes:
                res = cl.request_data(vehicle, dnode, start, stop)
                print(res)
                if not start and stop:
                    #single value
                    res_list[vehicle][dnode] = res[2][0]['v']
                else:
                    res_list[vehicle][dnode] = res[2]
    except(Exception):
        raise Exception("Error in getting data")
    
    return res_list

def get_available_vehicles():
    """
    look up available vehicles from awesomeIOT/res
    
    Returns: 
        vehicle (list(string)) : List of vehicleIDs
        
    TODO:
        Get dnode listing from api instead of static csv file?
    """
#    vehicles = ["133353",
#            "137859",
#            "174460",
#            "186973",
#            "192487",
#            "192493"]
    
    data = pd.read_csv('./iotviewer/res/datanode_mapping.csv')
    vehicles = data['Asset'].apply(str).unique()
    return list(vehicles)
    
def get_available_datanodes():
    """
    look up available datanodes from iotviewer/res
    
    Returns: 
        dnodes (list(string)) : of available datanode cleartext names
    
    TODO:
        get dnodes from API instead of static CSV
    
    """
#    dnodes = ["Battery Total External Energy",
#              "Battery Total Charged Energy",
#              "Battery Total Discharged Energy",
#              "Drive Energy Generated",
#              "Drive Energy Used",
#              "Energy Drive Motor",
#              "Odometer",
#              ]
    
    data = pd.read_csv('./iotviewer/res/datanode_mapping.csv')
    dnodes = data['Name'].unique()
    #hack for quick test
    return list(dnodes)