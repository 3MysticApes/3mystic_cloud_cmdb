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
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key="extra_id")
        },
        "InstanceType":{
          "display": "Instance Type",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["properties","hardwareProfile","vmSize"])
        },
        "Platform":{
          "display": "Platform",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","osDisk","osType"])
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
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","sku"])]) 
        },
        "AMIName": {
          "display": "AMI Name",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ".", str_array= [self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","publisher"]), self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","sku"]), self.get_item_data_value(item_data= item, value_key=["properties","storageProfile","imageReference","version"])])
        },
        "AMIDescription": {
          "display": "AMI Description",
          "handler": lambda item: None
        },
        "LaunchTime":{
          "display": "LaunchTime",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_resource","createdTime"])
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
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_private_ips(vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "ProductCodes":{
          "display": "ProductCodes",
          "handler": lambda item: None
        },
        "PublicDnsName":{
          "display": "PublicDnsName",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_public_ips_fqdn(vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"]), vm_load_balancers= self.get_item_data_value(item_data= item, value_key=["extra_load_balancers"])))
        },
        "SubnetId":{
          "display": "SubnetId",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_subnets(vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
        },
        "VpcId":{
          "display": "VpcId",
          "handler": lambda item: self.get_common().helper_type().string().join(separator= ",", str_array= self._get_vm_vnets(vm_nics= self.get_item_data_value(item_data= item, value_key=["extra_nics"])))
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
          "handler": lambda item: self.generate_resource_tags_csv(tags= self.get_item_data_value(item_data= item, value_key=["tags"]))
        },
        "VirtualizationType":{
          "display": "VirtualizationType",
          "handler": lambda item: None
        },
        "AvailabilitySet":{
          "display": "AvailabilitySet",
          "handler": lambda item: self.get_item_data_value(item_data= item, value_key=["extra_availability_set", "name"])
        },
        "LBType":{
          "display": "LB Type",
          "handler": lambda item: None # self.get_common().helper_type().string().join(separator= "-", 
            # str_array= [
            #   self.get_item_data_value(item_data= item, value_key=["extra_load_balancers", "load_balancer", "sku", "name"]),
            #   self.get_item_data_value(item_data= item, value_key=["extra_load_balancers", "load_balancer", "sku", "tier"])
            # ])
        },
        "LBDNSName":{
          "display": "LB DNS Name",
          "handler": lambda item: None # Pending
        },
        "LBName":{
          "display": "LB Name",
          "handler": lambda item: None #
          # [
          #   self.get_item_data_value(item_data= item_lb, value_key=["extra_load_balancers", "name"])
          #   for item_lb in self.get_item_data_value(item_data= item, value_key=["extra_load_balancers"])
          # ]
        },
      } 
    }
  
  def _get_vm_vnets(self, vm_nics, *args, **kwargs):
    subnets = self._get_vm_subnets(vm_nics= vm_nics)

    if subnets is None:
      return []
    
    vnet_ids = []
    for subnet in subnets:
      subnet_lower = self.get_common().helper_type().string().set_case(string_value= subnet, case= "lower")
      vnet_ids.append(subnet_lower[0:subnet_lower.rfind("/subnets/")])
    
    return vnet_ids
  
  def _get_vm_subnets(self, vm_nics, *args, **kwargs):
    if hasattr(self, "_vm_subnets"):
      return self._vm_subnets

    if vm_nics is None:
      return []
    
    self._vm_subnets = []
    for nic in vm_nics:
      ip_configurations = self.get_item_data_value(item_data= nic, value_key=["properties","ip_configurations"])
      if ip_configurations is None:
        continue
      
      for ip_config in ip_configurations:
        if ip_config.get("subnet") is None:
          continue
        self._vm_subnets.append(self.get_cloud_client().get_resource_id_from_resource(resource= ip_config.get("subnet")))
    
    return self._get_vm_subnets(vm_nics= vm_nics)
  
  def _get_vm_private_ips(self, vm_nics, *args, **kwargs):

    if vm_nics is None:
      return []
    
    
    return [
      ip_config.get("private_ip_address") 
      for ip_config in self._get_vm_nic_ip_configurations(vm_nics= vm_nics)
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= ip_config.get("private_ip_address") )
    ]
  
  def _get_vm_nic_ip_configurations(self, vm_nics, *args, **kwargs):    
    if hasattr(self, "_vm_nic_ip_configurations"):
      return self._vm_nic_ip_configurations
    
    if vm_nics is None:
      return []
    
    self._vm_nic_ip_configurations = []
    for nic in vm_nics:
      ip_configurations = self.get_item_data_value(item_data= nic, value_key=["properties","ip_configurations"])
      if ip_configurations is None:
        continue
      
      self._vm_nic_ip_configurations += [ip_config for ip_config in ip_configurations]

    
    return self._get_vm_nic_ip_configurations(vm_nics= vm_nics, *args, **kwargs)
  
  def _get_vm_public_ips_fqdn(self, vm_nics, vm_load_balancers, *args, **kwargs):
    for public_ip in self._get_vm_public_ips(vm_nics= vm_nics, vm_load_balancers= vm_load_balancers):
      print(public_ip)
    return [
      public_ip.dns_settings.fqdn
      for public_ip in self._get_vm_public_ips(vm_nics= vm_nics, vm_load_balancers= vm_load_balancers)
    ]
  
  def _get_vm_public_ips_ip(self, vm_nics, vm_load_balancers, *args, **kwargs):
    return [
      public_ip.ip_address
      for public_ip in self._get_vm_public_ips(vm_nics= vm_nics, vm_load_balancers= vm_load_balancers)
    ]       

    return public_ips

  
  def _get_vm_public_ips_vm_load_balancers(self, vm_load_balancers, *args, **kwargs):
    if hasattr(self, "_vm_load_balancers"):
      return self._vm_load_balancers

    if vm_load_balancers is None:
      return []

    self._vm_load_balancers = []
    for load_balancer in vm_load_balancers:
      if self.get_item_data_value(item_data= load_balancer, value_key=["extra_public_ips"]) is None:
        continue

      for ip in self.get_item_data_value(item_data= nic, value_key=["extra_public_ips"]):
        self._vm_load_balancers.append(ip)

    return self._get_vm_public_ips_vm_load_balancers(vm_load_balancers= vm_load_balancers, *args, **kwargs)

  
  def _get_vm_public_ips_vm_nics(self, vm_nics, *args, **kwargs):
    if hasattr(self, "_vm_nic_public_ips"):
      return self._vm_nic_public_ips

    if vm_nics is None:
      return []

    self._vm_nic_public_ips = []
    for nic in vm_nics:
      if self.get_item_data_value(item_data= nic, value_key=["extra_public_ips"]) is None:
        continue

      for ip in self.get_item_data_value(item_data= nic, value_key=["extra_public_ips"]):
        self._vm_nic_public_ips.append(ip)

    return self._get_vm_public_ips_vm_nics(vm_nics= vm_nics, *args, **kwargs)

  def _get_vm_public_ips(self, vm_nics, vm_load_balancers, *args, **kwargs):
    if hasattr(self, "_vm_public_ips"):
      return self._vm_public_ips

    if vm_nics is None and vm_load_balancers is None:
      return []
    
    # ip_address
    # dns_settings.fqdn
    self._vm_public_ips = (
      self._get_vm_public_ips_vm_nics(vm_nics= vm_nics) +
      self._get_vm_public_ips_vm_load_balancers(vm_load_balancers= vm_load_balancers)
    )        

    
    return self._get_vm_public_ips(vm_nics= vm_nics, vm_load_balancers= vm_load_balancers, *args, **kwargs)
