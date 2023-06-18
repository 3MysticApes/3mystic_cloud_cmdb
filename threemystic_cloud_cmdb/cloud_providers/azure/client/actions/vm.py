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
          "handler": lambda item: item["instance"].id if item.get("instance") is not None and item["instance"] and common.is_type(item["instance"], VirtualMachine) else None
        },
        "InstanceType":{
          "display": "Instance Type",
          "handler": lambda item: item["instance"].hardware_profile.vm_size if item.get("instance") is not None and item["instance"] and common.is_type(item["instance"], VirtualMachine) else None
        },
        "Platform":{
          "display": "Platform",
          "handler": lambda item: item["instance"].storage_profile.os_disk.os_type if item.get("instance") is not None else None
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
          "handler": lambda item: get_ami_id(item["instance"]) if item.get("instance") is not None else None
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: get_ami_name(item["instance"]) if item.get("instance") is not None else None
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "LaunchTime":{
          "display": "LaunchTime",
          "handler": lambda item: item["resource"].created_time.replace(tzinfo=None) if item.get("resource") is not None and item.get("resource").created_time is not None else None
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
          "handler": lambda item: get_vm_privateip(item.get("nics"))
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
          "handler": lambda item: get_vm_subnet_id(item.get("nics"))
        },
        "VpcId":{
          "display": "VpcId",
          "handler": lambda item: get_vm_vnet_ids(item.get("nics"))
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
          "handler": lambda item: json.dumps(item["instance"].tags) if item.get("instance") is not None else None
        },
        "VirtualizationType":{
          "display": "VirtualizationType",
          "handler": lambda item: None
        },
        "AvailabilitySet":{
          "display": "AvailabilitySet",
          "handler": lambda item: item["availability_set"].name if item.get("availability_set") is not None else None
        },
        "LBType":{
          "display": "LB Type",
          "handler": lambda item: (f'{item["lb"][0].sku.name}-{item["lb"][0].sku.tier}') if item.get("lb") is not None and len(item.get("lb")) > 0 and item.get("lb")[0].sku is not None else None
        },
        "LBDNSName":{
          "display": "LB DNS Name",
          "handler": lambda item: item["public_ip"].dns_settings.fqdn if item.get("public_ip") is not None and item["public_ip"].dns_settings is not None else None
        },
        "LBName":{
          "display": "LB Name",
          "handler": lambda item: (item["lb"][0].name) if item.get("lb") is not None and len(item.get("lb")) > 0 else None
        },
      } 
    }