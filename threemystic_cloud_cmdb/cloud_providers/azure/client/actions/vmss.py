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
          "handler": lambda item: item["asg"].id if item.get("asg") is not None and item["asg"] and common.is_type(item["asg"], VirtualMachineScaleSet) else None
        },
        "ASGName": {
          "display": "ASG Name",
          "handler": lambda item: item["asg"].name if item.get("asg") is not None and item["asg"] and common.is_type(item["asg"], VirtualMachineScaleSet) else None
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
          "handler": lambda item: item["asg"].sku.capacity if item.get("asg") is not None and item["asg"] and common.is_type(item["asg"], VirtualMachineScaleSet) else None
        },
        "ASGEffective": {
          "display": "Effective",
          "handler": lambda item: None
        },
        "InstanceType": {
          "display": "Instance Type",
          "handler": lambda item: item["asg"].sku.name if item.get("asg") is not None and item["asg"] and common.is_type(item["asg"], VirtualMachineScaleSet) else None
        },
        "AMIID": {
          "display": "AMI ID",
          "handler": lambda item: get_ami_id(item["asg"]) if item.get("asg") is not None and item["asg"] and common.is_type(item["asg"], VirtualMachineScaleSet) else None
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: get_ami_name(item["asg"]) if item.get("asg") is not None and item["asg"] and common.is_type(item["asg"], VirtualMachineScaleSet) else None
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: common.generate_resource_tags_csv(tags=item["asg"].tags) if item.get("asg") is not None and item["asg"].tags is not None else None
        },
    }
    }