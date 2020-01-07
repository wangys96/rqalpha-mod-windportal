import numpy as np

from collections import namedtuple

DBItem = namedtuple("Item", ["dtype", "wind_field", ])

class Configuration(dict):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self._default_fields = list(self["default_fields"].keys()) 
        self._all_fields = self._default_fields + list(self["fields"].keys()) 

        self._default_dtypes = [(f, item.dtype) for f,item in self["default_fields"].items()] 
        self._all_dtypes = np.dtype(self._default_dtypes + [(f, item.dtype) for f,item in self["fields"].items()])

        self._default_wind_fields = ",".join([item.wind_field for f,item in self["default_fields"].items()])
        self._all_wind_fields = self._default_wind_fields + "," + ",".join([item.wind_field for f,item in self["fields"].items()])                              

    def get_fields(self, fields=None):
        if fields:
            return self._default_fields + [f for f in fields if f in self["fields"] and f not in self["default_fields"]]
        return self._all_fields

    def get_dtypes(self, fields=None):
        if fields:
            return np.dtype(self._default_dtypes + [(f, self["fields"][f].dtype) for f in fields 
                                            if f in self["fields"] and f not in self["default_fields"]])
        return self._all_dtypes

    def get_wind_fields(self,fields=None):
        if fields:
            return self._default_wind_fields + "," + ",".join([self["fields"][f].wind_field for f in fields 
                                                    if f in self["fields"] and f not in self["default_fields"]])
        return self._all_wind_fields
    
    def convert(self, result):
        for f in result.dtype.names:
            if f in self["converts"]:
                result[f] = self["converts"][f](result[f])
        return result


StockConfiguration = Configuration(
    {
        "default_fields":{
            "datetime":DBItem("<u8", "TRADE_DT"),
        },
        "fields":{
            "open": DBItem("<f8", "S_DQ_OPEN"),
            "close": DBItem("<f8", "S_DQ_CLOSE"),
            "high": DBItem("<f8", "S_DQ_HIGH"),
            "low": DBItem("<f8", "S_DQ_LOW"),
            "volume": DBItem("<f8", "S_DQ_VOLUME"),
            "total_turnover": DBItem("<f8", "S_DQ_AMOUNT"),
            "limit_up": DBItem("<f8", "S_DQ_PRECLOSE*1.1"),
            "limit_down": DBItem("<f8", "S_DQ_PRECLOSE*0.9"),
        },
        "converts":{
            "datetime":lambda x : x*1000000
        }
    }
)

IndexConfiguration = Configuration(
    {
        "default_fields":{
            "datetime":DBItem("<u8", "TRADE_DT"),
        },
        "fields":{
            "open": DBItem("<f8", "S_DQ_OPEN"),
            "close": DBItem("<f8", "S_DQ_CLOSE"),
            "high": DBItem("<f8", "S_DQ_HIGH"),
            "low": DBItem("<f8", "S_DQ_LOW"),
            "volume": DBItem("<f8", "S_DQ_VOLUME"),
            "total_turnover": DBItem("<f8", "S_DQ_AMOUNT"),
        },
        "converts":{
            "datetime":lambda x : x*1000000
        }
    }
)

AdjConfiguration = Configuration(
    {
        "default_fields":{
            "start_date":DBItem("<u8", "TRADE_DT"),
        },
        "fields":{
            "ex_cum_factor": DBItem("<f8", "S_DQ_ADJFACTOR")
        },
        "converts":{
            "start_date":lambda x : x*1000000
        }
    }
)