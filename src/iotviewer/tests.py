from .models import DataPoint
from .models import Dataset
from .models import DatasetArray
import unittest

class ModelsTest(unittest.TestCase):
    
    def test_table_headers_are_rendered_correctly(self):
        pass
    
    def test_dataset_serialization(self):
        dp1 = DataPoint(1, 2)
        dp2 = DataPoint(4, 7)
        
        dset = Dataset(label="TestDataset", data=[dp1, dp2])
        
        dset_ser = dset.serialize()
        assert dset_ser == "{data: [{x : 1, y : 2 },{x : 4, y : 7 },], label: 'TestDataset', borderColor: '#3e95cd', fill: false, showLine: true}"

    def test_dataset_array_serialization(self):
        
        dp1 = DataPoint(1, 2)
        dset1 = Dataset(label="TestDataset", data=[dp1])

        dp2 = DataPoint(4, 7)
        dset2 = Dataset(label="TestDataset", data=[dp2])
        
        ds_array = DatasetArray(datasets=[dset1, dset2])
        
        ser = ds_array.serialize()
        
        assert ser == "[{data: [{x : 1, y : 2 },], label: 'TestDataset', borderColor: '#3e95cd', fill: false, showLine: true},{data: [{x : 4, y : 7 },], label: 'TestDataset', borderColor: '#3e95cd', fill: false, showLine: true},]"

    def test_datasets_not_persisted_between_consecutive_calls(self):
        assert False