from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="vmss", 
      logger_name= "cloud_cmdb_azure_client_action_vmss", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
    
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    return {
      "ASG":{
        "display":"ASG",
      }
    }
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    return {
      "ASG": {
        "AutoScalingGroup":{
          "display": "AutoScalingGroup",
          "handler": lambda item: "VMSS"
        },        
        "ASGArn": {
          "display": {"default": "ID", "cmdb":"ASG Arn"},
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="extra_id")
        },
        "ASGName": {
          "display": "Name",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="name")
        },
        "ASGMin": {
          "display": "Min",
          "handler": lambda item: None
        },
        "ASGDesiredCapacity": {
          "display": "Desired",
          "handler": lambda item: None
        },
        "ASGMaxSize": {
          "display": "Max",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["sku", "capacity"])
        },
        "ASGEffective": {
          "display": "Effective",
          "handler": lambda item: None
        },
        "InstanceType": {
          "display": "Instance Type",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["sku", "name"])
        },
        "AMIID": {
          "display": "AMI ID",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","sku"])]) 
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","sku"]), self.get_item_data_value(item_data= item, value_key=["properties", "virtualMachineProfile", "storageProfile","imageReference","version"])])  
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= self.get_item_data_value(item_data= item, value_key=["tags"]))
        },
      }
    }