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
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["type"])
        },
        "Identifier":{
          "display": "Identifier",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_id"])
        },
        "Name":{
          "display": "Name",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["name"])
        },
        "Size":{
          "display": "Size_Gib",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["diskSizeGB"])
        },
        "Attached":{
          "display": "Attached",
          "handler": lambda item:  self.get_item_data_value(item_data= item, value_key=["diskState"])
        },
        "GroupType":{
          "display": "GroupType",
          "handler": lambda item: None # item["Storage"].get("group_type") if item["Storage"] is not None and item["Storage"].get("group_type") else None
        },
        "Group":{
          "display": "Group",
          "handler": lambda item: None # item["Storage"].get("group") if item["Storage"] is not None and item["Storage"].get("group") else None
        },
        "GroupPrimary":{
          "display": "GroupPrimary",
          "handler": lambda item: None # item["Storage"].get("group_primary") if item["Storage"] is not None and item["Storage"].get("group_primary") else None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= self.get_item_data_value(item_data= item, value_key=["tags"]))
        },
      } 
    }