from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from decimal import Decimal, ROUND_HALF_UP
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import GranularityType,ForecastDefinition,ForecastType,ForecastTimeframe,ForecastTimePeriod,QueryDefinition,TimeframeType,ExportType,QueryTimePeriod


class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="budget", 
      logger_name= "cloud_cmdb_azure_client_action_budget", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    return {
      "Budget":{
        "display":"Budget",
        "include_region": False,
        "include_resourcegroup": False,
        "include_requiredtags": False
      }
    }
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    return {
      "Budget": {
        "last_seven_days":{
          "display": "Last7Days",
          "handler": lambda item: item["last_seven_days"] if item.get("last_seven_days") is not None else ""
        },
        "month_to_date":{
          "display": "MonthToDate",
          "handler": lambda item: item["month_to_date"] if item.get("month_to_date") is not None else ""
        },
        "month_forecast":{
          "display": "MonthTotalForcast",
          "handler": lambda item: item["month_forecast"] if item.get("month_forecast") is not None else ""
        },
        "year_to_date":{
          "display": "YearToDate",
          "handler": lambda item: item["year_to_date"] if item.get("year_to_date") is not None else ""
        },
        "year_forecast":{
          "display": "YearTotalForcast",
          "handler": lambda item: item["year_forecast"] if item.get("year_forecast") is not None else ""
        },
      } 
    }
 