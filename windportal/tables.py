# -*- coding: utf-8 -*-
import six
import numpy as np
import pandas as pd

from copy import copy
from rqalpha.utils.py2 import lru_cache
from rqalpha.utils.i18n import gettext as _
from rqalpha.model.instrument import Instrument

from .wind_utils import _wc

class DayBarTable(object):
    def __init__(self, table, connection, config):
        self._table = table
        self._conn = connection
        self._config = config

    def get_bars(self, order_book_id, fields=None):
        order_book_id = _wc(order_book_id)
        dtypes = self._config.get_dtypes(fields)
        wind_fields = self._config.get_wind_fields(fields)

        query = """
                SELECT {}
                 FROM {} A
                 WHERE S_INFO_WINDCODE='{}'
                 ORDER BY TRADE_DT ASC
                """.format(wind_fields, self._table, order_book_id)

        with self._conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        
        if len(result) == 0:
            six.print_(_(u"No data for {}").format(order_book_id))
            return np.empty(0, dtype=dtypes)

        return self._config.convert(np.array(result, dtype=dtypes))

    def get_date_range(self, order_book_id):
        order_book_id = _wc(order_book_id)
        query = """
                SELECT MIN(TRADE_DT),MAX(TRADE_DT)
                 FROM {} A
                 WHERE S_INFO_WINDCODE='{}'
                """.format(self._table, order_book_id)

        with self._conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        
        if len(result) == 0:
            raise IndexError(f"{order_book_id} has no records")
            
        return result[0][0], result[0][1]

class SimpleFactorTable(object):
    def __init__(self, table, connection, config):
        self._table = table
        self._conn = connection
        self._config = config

    def get_factors(self, order_book_id):
        order_book_id = _wc(order_book_id)
        dtypes = self._config.get_dtypes(None)
        wind_fields = self._config.get_wind_fields(None)

        query = """
                SELECT {}
                 FROM {} A
                 WHERE S_INFO_WINDCODE='{}'
                 ORDER BY TRADE_DT ASC
                """.format(wind_fields, self._table, order_book_id)

        with self._conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()

        if len(result) == 0:
            raise IndexError(f"{order_book_id} has no records")

        result = np.array(result, dtype=dtypes)
        idx = np.ones(result.shape)
        idx[1:] = np.diff(result[result.dtype.names[1]])
        return self._config.convert(result[idx!=0])

class TradingDatesTable(object):
    def __init__(self, table, connection, config):
        self._table = table
        self._conn = connection
        self._config = config
        query = """
                SELECT TRADE_DAYS
                 FROM {} A
                 WHERE S_INFO_EXCHMARKET='SSE'
                 ORDER BY TRADE_DAYS ASC
                """.format(self._table) 

        with self._conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()

        self._dates = pd.DatetimeIndex(np.array(result).reshape(len(result)))
        
    def get_trading_calendar(self):
        return self._dates

class DateTable(object):
    def __init__(self, table, connection, config):
        self._table = table
        self._conn = connection
        self._config = config

    @lru_cache(None)
    def get_days(self, order_book_id):
        query = """
                SELECT S_DQ_SUSPENDDATE
                 FROM {} A
                 WHERE (S_DQ_SUSPENDTYPE=444016000 OR S_DQ_SUSPENDTYPE=444003000)
                       AND S_INFO_WINDCODE='{}'
                 ORDER BY S_DQ_SUSPENDDATE ASC
                """.format(self._table, _wc(order_book_id))

        with self._conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()

        if len(result)==0: return {}

        return {int(x[0]) for x in result}
        #return np.array(result,dtype="<u8").reshape(len(result))

    def contains(self, order_book_id, dates):
        date_set = self.get_days(order_book_id)

        if len(date_set)==0:
            return [False] * len(dates)

        def _to_dt_int(d):
            if isinstance(d, (int, np.int64, np.uint64)):
                return int(d // 1000000) if d > 100000000 else int(d)
            else:
                return d.year*10000 + d.month*100 + d.day

        return [(_to_dt_int(d) in date_set) for d in dates]