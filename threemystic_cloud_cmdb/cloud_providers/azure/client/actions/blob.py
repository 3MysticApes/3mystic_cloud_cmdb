from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from azure.mgmt.storage import StorageManagementClient

class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="blob", 
      logger_name= "cloud_cmdb_azure_client_action_blob", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    return {
      "BlobStorage":{
        "display":"BlobStorage",
      }
    }
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    return {
      "BlobStorage": {
        "Service":{
          "display": "Service",
          "data_key": "extra_raw_item"
          "handler": lambda item: (item["extra_raw_item"] if item.get("extra_raw_item") is not None else item)["sku"]["name"]
        },
        "BucketContainer":{
          "display": "BucketContainer",
          "handler": lambda item: (item["extra_raw_item"] if item.get("extra_raw_item") is not None else item)["name"]  
        },
        "BucketName":{
          "display": "BucketName",
          "handler": lambda item: item["name"] if item.get("extra_raw_item") is not None else None
        },
        "AvgSizeLast24HR_Bytes":{
          "display": "AvgSizeLast24HR_Bytes",
          "handler": lambda item:  None
        },
        "SampleObjectClass":{
          "display": "SampleObjectClass",
          "handler": lambda item: None
        },
        "SampleObjectRetention":{
          "display": "SampleObjectRetention",
          "handler": lambda item: None
        },
        "Encryption":{
          "display": "Encryption",
          "handler": lambda item: None
        },
        "Versioning":{
          "display": "Versioning",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: common.generate_resource_tags_csv(tags=item["Tags"])
        },
      } 
    }