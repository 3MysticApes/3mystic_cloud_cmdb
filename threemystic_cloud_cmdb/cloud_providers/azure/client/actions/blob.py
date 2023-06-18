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
          "handler": lambda item: (item if item is not None else {}).get("extra_storage_account").get("sku").get("name")
        },
        "BucketContainer":{
          "display": "BucketContainer",
          "handler": lambda item: (item if item is not None else {}).get("extra_storage_account").get("name") 
        },
        "BucketName":{
          "display": "BucketName",
          "handler": lambda item: (item if item is not None else {}).get("name") 
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
          "handler": lambda item: (item if item is not None else {}).get("encryption").get("services").get("blob").get("enabled")
        },
        "Versioning":{
          "display": "Versioning",
          "handler": lambda item: (item if item is not None else {}).get("immutable_storage_with_versioning")
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags=(item if item is not None else {}).get("extra_storage_account").get("tags"))
        },
      } 
    }