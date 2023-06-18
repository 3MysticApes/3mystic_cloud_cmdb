from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio

class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="storage", 
      logger_name= "cloud_cmdb_azure_client_action_storage", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    return {
      "Storage":{
        "display":"Storage",
      }
    }
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    return {
      "Storage": {
        "Type":{
          "display": "StorageType",
          "handler": lambda item: item["Storage"].get("type") if item["Storage"] is not None and item["Storage"].get("type") else None
        },
        "Identifier":{
          "display": "Identifier",
          "handler": lambda item: item["Storage"].get("id") if item["Storage"] is not None and item["Storage"].get("id") else None
        },
        "Name":{
          "display": "Name",
          "handler": lambda item: item["Storage"].get("name") if item["Storage"] is not None and item["Storage"].get("name") else None
        },
        "Size":{
          "display": "Size_Gib",
          "handler": lambda item: item["Storage"].get("size") if item["Storage"] is not None and item["Storage"].get("size") else None
        },
        "Attached":{
          "display": "Attached",
          "handler": lambda item: item["Storage"].get("attached") if item["Storage"] is not None and item["Storage"].get("attached") else None
        },
        "GroupType":{
          "display": "GroupType",
          "handler": lambda item: item["Storage"].get("group_type") if item["Storage"] is not None and item["Storage"].get("group_type") else None
        },
        "Group":{
          "display": "Group",
          "handler": lambda item: item["Storage"].get("group") if item["Storage"] is not None and item["Storage"].get("group") else None
        },
        "GroupPrimary":{
          "display": "GroupPrimary",
          "handler": lambda item: item["Storage"].get("group_primary") if item["Storage"] is not None and item["Storage"].get("group_primary") else None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: common.generate_resource_tags_csv(tags=item["Tags"]) if item["Tags"] is not None else None
        },
      } 
    }