import pandas as pd
from datetime import datetime as dtm
def _wc(rqcode):
    return rqcode.replace("XSHE","SZ").replace("XSHG","SH")

def update_instrument(connection):
    query = """
            SELECT S_INFO_WINDCODE,S_INFO_NAME,S_INFO_LISTDATE,S_INFO_DELISTDATE,S_INFO_EXCHMARKET
            FROM Wind.AShareDescription
            ORDER BY S_INFO_WINDCODE ASC
            """
    with connection.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
    result

    data = pd.DataFrame(result,columns=["wind_code","symbol","listed_date","de_listed_date","exchange"])
    data.loc[:,"code"] = data["wind_code"].apply(lambda code:code[:6])
    data.loc[:,"exchange"] = data["exchange"].apply(lambda x:"XSHE"if x=="SZSE" else "SSE")
    data.set_index("code",inplace=True)
    data.loc[data.listed_date.isnull(),"listed_date"]="19900101"
    data.loc[:,"listed_date"]=pd.to_datetime(data["listed_date"])
    data.loc[data.de_listed_date.isnull(),"de_listed_date"]="29991231"
    data.loc[:,"de_listed_date"]=data["de_listed_date"].apply(lambda s:dtm(int(s[:4]),int(s[4:6]),int(s[6:])))
    data["order_book_id"] = data["wind_code"].apply(lambda code:code[:7]+"XSHE"if code[-2:]=="SZ" else code[:7]+"XSGE")