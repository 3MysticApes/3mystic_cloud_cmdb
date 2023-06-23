from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers



class cloud_cmdb_general_config_step_2_cloud_share(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_2_cloud_share", *args, **kwargs)
    

  def step(self, cloud_share= None, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= cloud_share):
      return
    
    if cloud_share == cloud_share:
      self._step_ms365(cloud_share= cloud_share)
      return
  
  def get_tenant_id_index(self, data_client, cloud_share):
    try:
      index = 1
      for tenant in data_client.get_cloud_client().get_tenants():
        if data_client.get_cloud_client().get_tenant_id(tenant= tenant) == self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id'):
          return index
        index += 1
    except:
      pass

    return None
    
  def _step_ms365(self, cloud_share, *args, **kwargs):
    from threemystic_cloud_data_client.cloud_data_client import cloud_data_client
    data_client = cloud_data_client(
      provider= "azure",
      logger= self.get_logger(), 
      common= self.get_common()      
    ).client(suppress_parser_help= True)

    # ms_graph = self.get_common().graph().graph(graph_method= "msgraph", credentials= data_client.get_cloud_client().get_tenant_credential(tenant= "425a5546-5a6e-4f1b-ab62-23d91d07d893"))
    # print(ms_graph.send_request(
    #   url = ms_graph.generate_graph_url(resource= "me")
    # ))
    print("-----------------------------")
    print()
    print("What tenant will store the cmdb data?")
    print()
    print("-----------------------------")
    
    
    index = 1
    print("loading tenants")
    data_client.get_cloud_client().get_tenants()
    print(f"0: Remove Entry")
    for tenant in data_client.get_cloud_client().get_tenants():
      print(f"{index}: {data_client.get_cloud_client().get_tenant_id(tenant= tenant)}")
      index += 1

    tenant_index = self.get_tenant_id_index(data_client= data_client, cloud_share= cloud_share)
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "tenant_id": {
          "validation": lambda item: self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= len(data_client.get_cloud_client().get_tenants()),
          "messages":{
            "validation": f"Valid options are: 0 - {len(data_client.get_cloud_client().get_tenants())}",
          },
          "conversion": lambda item: self.get_common().helper_type().int().get(item),
          "desc": f"Please select the tenant to use \nValid Options: 0 - {len(data_client.get_cloud_client().get_tenants())}",
          "default": tenant_index,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": tenant_index is not None
        },
      }
    )

    if(response is not None):
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= response.get("tenant_id").get("formated")):
        self.get_cloud_share_config_value(
          config_key= cloud_share
        )["tenant_id"] = data_client.get_cloud_client().get_tenant_id(tenant= data_client.get_cloud_client().get_tenants()[response.get("tenant_id").get("formated") - 1]) if response.get("tenant_id").get("formated") > 0 else ""
        self._save_config_cloud_share()

        print("-----------------------------")
        print()
        print(f"Tenant ID Updated: {self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id')}")
        print()
        print("-----------------------------")

    
  
    
  
