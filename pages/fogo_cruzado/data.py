import calendar
from datetime import datetime
import pandas as pd
import pytz


def utc_to_local(utc_dt: datetime) -> datetime:
    local_tz = pytz.timezone('America/Sao_Paulo')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def get_day_period(date: datetime) -> str:
    if 0 <= date.hour < 6:
        return "MADRUGADA"
    
    if 6 <= date.hour < 12:
        return "MANHÃ" 
    
    if 12 <= date.hour < 18:
        return "TARDE"
    
    # if 18 <= date.hour < 24:    
    return "NOITE"


def normalize_occurrences_data(occurrences: list[dict]) -> pd.DataFrame:
    data = []
    for occur in occurrences:    
        try:
            locality = occur.get("locality", {})
            if locality: 
                locality = locality.get("name", None)
            
            neighborhood = occur.get("neighborhood", {})
            if neighborhood:
                neighborhood = neighborhood.get("name", None)
                
            sub_neighborhood = occur.get("subNeighborhood", {})
            if sub_neighborhood:
                sub_neighborhood = sub_neighborhood.get("name", None)
                
            context_info = occur.get("contextInfo", {})
            if context_info:
                reason = context_info.get("mainReason", {})
                if reason:
                    reason = reason.get("name", None)
                
                massacre = context_info.get("massacre", False)
                
            date = occur.get("date", None)
            datetime_string = None
            date_string = None
            time_string = None
            month_number = None
            month_name = None
            month_name_abbr = None
            day_period = None
            if date:
                date = utc_to_local(datetime.fromisoformat(date))
                datetime_string = date.strftime("%d/%m/%Y, %H:%M:%S")
                date_string = date.strftime("%d/%m/%Y")
                time_string = date.strftime("%H:%M:%S")
                month_number = date.month
                month_name = calendar.month_name[date.month]
                month_name_abbr = calendar.month_abbr[date.month]
                day_period = get_day_period(date)
            
            date = {} if date is None else date
            
            victims = occur.get("victims", [])
            if not victims:
                victims = []
        
            data.append({
                'id': occur.get("id", None),
                "city": occur.get("city", {}).get("name", None),
                "locality": locality,
                "neighborhood": neighborhood,
                "sub_neighborhood": sub_neighborhood,
                "latitude": occur.get("latitude", None),
                "longitude": occur.get("longitude", None),
                "datetime_string": datetime_string,
                "date_string": date_string,
                "time_string": time_string,
                "month_number": month_number,
                "month_name": month_name,
                "month_name_abbr": month_name_abbr,
                "day_period": day_period,
                "reason": reason,
                "massacre": massacre,
                "police_presence": occur.get("policeAction", None),
                "security_agent_presence": occur.get("agentPresence"),
                "victims": victims,
                "victims_quantity": len(victims)
            })
        except TypeError as e:
            print("Occurrence empty")

    return data


def build_occurrences_df(occurrences_data: list[dict]) -> pd.DataFrame:
    data = []
    for occur in occurrences_data:
        data.append({
            "id": occur["id"],
            "city": occur["city"],
            "locality": occur["locality"],
            "neighborhood": occur["neighborhood"],
            "sub_neighborhood": occur["sub_neighborhood"],
            "latitude": occur["latitude"],
            "longitude": occur["longitude"],
            "datetime": occur["datetime_string"],
            "time": occur["time_string"],
            "month_number": occur["month_number"],
            "month_name": occur["month_name"],
            "month_name_abbr": occur["month_name_abbr"],
            "day_period": occur["day_period"],
            "reason": occur["reason"],
            "massacre": occur["massacre"],
            "police_presence": occur["police_presence"],
            "security_agent_presence": occur["security_agent_presence"],
            "victims_quantity": occur["victims_quantity"]
        })
    df = pd.DataFrame(data, columns=[
        "id", 
        "city", 
        "locality", 
        "neighborhood", 
        "sub_neighborhood", 
        "latitude", "longitude", 
        "datetime", "time", "month_number", "month_name", "month_name_abbr", "day_period",
        "reason", "massacre", "police_presence", "security_agent_presence", "victims_quantity"])
    return df

    