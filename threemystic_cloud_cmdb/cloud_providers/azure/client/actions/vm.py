from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="vm", 
      logger_name= "cloud_cmdb_azure_client_action_vm", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
    
  
  def _load_cmdb_general_data(self, *args, **kwargs):
    return {
      "LongLived":{
        "display":"LongLived",
      }
    }
  
  def _load_cmdb_column_data(self, *args, **kwargs):
    return {
      "LongLived": {
        "EC2":{
          "display": "EC2",
          "handler": lambda item: "VM"
        },
        "InstanceID":{
          "display": "Instance ID",
          "handler": lambda item: (item if item is not None else {}).get("extra_id")
        },
        "InstanceType":{
          "display": "Instance Type",
          "handler": lambda item: (item if item is not None else {}).get("properties").get("hardwareProfile").get("vmSize")
        },
        "Platform":{
          "display": "Platform",
          "handler": lambda item: (item if item is not None else {}).get("properties").get("storageProfile").get("osDisk").get("osType")
        },
        "PlatformName":{
          "display": "Platform Name",
          "handler": lambda item: None
        },
        "PlatformVersion":{
          "display": "Platform Version",
          "handler": lambda item: None
        },
        "IAMRole":{
            "display": "IAM Role",
            "handler": lambda item: None
        },
        "SSMPingStatus":{
          "display": "SSM Ping Status",
          "handler": lambda item: None
        },
        "SSMLastPingTime":{
          "display": "SSM Last Ping Time",
          "handler": lambda item: None
        },
        "SSMVersion":{
          "display": "SSM Version",
          "handler": lambda item: None
        },
        "AMIID": {
          "display": "AMI ID",
          "handler": lambda item: None # f'{item.get("properties").get("storageProfile").get("imageReference").get("publisher")}.{item.get("properties").get("storageProfile").get("imageReference").get("sku")}'
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: None # f'{item.get("properties").get("storageProfile").get("imageReference").get("publisher")}.{item.get("properties").get("storageProfile").get("imageReference").get("sku")}.{item.get("properties").get("storageProfile").get("imageReference").get("version")}'
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "LaunchTime":{
          "display": "LaunchTime",
          "handler": lambda item: (item if item is not None else {}).get("properties").get("timeCreated") # Check this changed
        }, 
        "Monitoring":{
          "display": "Monitoring",
          "handler": lambda item: None
        },
        "Tenancy":{
          "display": "Tenancy",
          "handler": lambda item: None
        },
        "PrivateDnsName":{
          "display": "PrivateDnsName",
          "handler": lambda item: None
        },
        "PrivateIpAddress":{
          "display": "PrivateIpAddress",
          "handler": lambda item: None # Pending
        },
        "ProductCodes":{
          "display": "ProductCodes",
          "handler": lambda item: None
        },
        "PublicDnsName":{
          "display": "PublicDnsName",
          "handler": lambda item: None
        },
        "SubnetId":{
          "display": "SubnetId",
          "handler": lambda item: None # Pending
        },
        "VpcId":{
          "display": "VpcId",
          "handler": lambda item: None # Pending
        },
        "Architecture":{
          "display": "Architecture",
          "handler": lambda item: None
        },
        "EbsOptimized":{
          "display": "EbsOptimized",
          "handler": lambda item: None
        },
        "Tags":{
          "display": "Tags",
          "handler": lambda item: self.generate_resource_tags_csv(tags= (item if item is not None else {}).get("tags"))
        },
        "VirtualizationType":{
          "display": "VirtualizationType",
          "handler": lambda item: None
        },
        "AvailabilitySet":{
          "display": "AvailabilitySet",
          "handler": lambda item: None # Pending 
        },
        "LBType":{
          "display": "LB Type",
          "handler": lambda item: None # Pending
        },
        "LBDNSName":{
          "display": "LB DNS Name",
          "handler": lambda item: None # Pending
        },
        "LBName":{
          "display": "LB Name",
          "handler": lambda item: None # Pending
        },
      } 
    }