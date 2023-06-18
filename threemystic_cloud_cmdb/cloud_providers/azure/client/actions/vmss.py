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
    
  
  def get_vmss_ami_name(vmss): 
    if vmss.get("virtualMachineProfile") is None:
      return None
    
    if vmss.get("virtualMachineProfile").get("storageProfile") is None:
      return None
    
    if vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference") is None:
      return None
    
    return f'{vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("publisher")}.{vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("sku")}'
  
  def get_vmss_ami_id(vmss): 
    if vmss.get("virtualMachineProfile") is None:
      return None
    
    if vmss.get("virtualMachineProfile").get("storageProfile") is None:
      return None
    
    if vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference") is None:
      return None
    
    return f'{vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("publisher")}.{vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("sku")}.{vmss.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("version")}'
  
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
          "handler": lambda item: (item if item is not None else {}).get("extra_id")
        },
        "ASGName": {
          "display": "Name",
          "handler": lambda item: (item if item is not None else {}).get("name")
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
          "handler": lambda item: (item if item is not None else {}).get("sku").get("capacity")
        },
        "ASGEffective": {
          "display": "Effective",
          "handler": lambda item: None
        },
        "InstanceType": {
          "display": "Instance Type",
          "handler": lambda item: (item if item is not None else {}).get("sku").get("name")
        },
        "AMIID": {
          "display": "AMI ID",
          "handler": lambda item: None # f'{item.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("publisher")}.{item.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("sku")}.{item.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("version")}'
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: None # f'{item.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("publisher")}.{item.get("virtualMachineProfile").get("storageProfile").get("imageReference").get("sku")}'
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= (item if item is not None else {}).get("tags"))
        },
      }
    }