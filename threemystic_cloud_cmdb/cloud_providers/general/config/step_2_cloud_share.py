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
      self._step_ms365_tenant(cloud_share= cloud_share)
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
    
  def _step_ms365_tenant(self, cloud_share, *args, **kwargs):
    from threemystic_cloud_data_client.cloud_data_client import cloud_data_client
    data_client = cloud_data_client(
      provider= "azure",
      logger= self.get_logger(), 
      common= self.get_common()      
    ).client(suppress_parser_help= True)

    
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
          "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= len(data_client.get_cloud_client().get_tenants()),
          "messages":{
            "validation": f"Valid options are: 0 - {len(data_client.get_cloud_client().get_tenants())}",
          },
          "conversion": lambda item: self.get_common().helper_type().int().get(item) if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) else item,
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

        self._step_ms365_tenant_location(cloud_share= cloud_share, data_client= data_client)
        return
      
    
    print("-----------------------------")
    print()
    print(f"Tenant ID NOT Updated")
    print()
    print("-----------------------------")

  
  def get_group_index(self, group_options, cloud_share):
    try:
      index = 0
      for group in group_options:
        if group.get("id") == self.get_cloud_share_config_value(config_key= cloud_share).get('group'):
          return index
        index += 1
    except:
      pass

    return None
  
  def _step_ms365_tenant_location(self, cloud_share, data_client, *args, **kwargs):

    print("-----------------------------")
    print()
    print("Where drive/group will the CMDB be stored in")
    print()
    print("-----------------------------")
    
    
    index = 1
    print("loading groups")
    group_options = [
      {
        "id": "Remove Entry"
      },      
      {
        "id": "@me"
      }
    ]

    ms_graph = self.get_common().graph().graph(graph_method= "msgraph", credentials= data_client.get_cloud_client().get_tenant_credential(tenant= self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id')))
    user_groups = ms_graph.send_request(
      url = ms_graph.generate_graph_url(resource= "me", base_path= "/transitiveMemberOf/microsoft.graph.group")
    )
    
    group_options = group_options + [
      {"id": group.get("id"), "display": f"{group.get('id')} - {group.get('displayName')}"} for group in user_groups.get("value")
    ]
    index = 0
    for option in group_options:
      if option.get("display") is not None:
        print(f'{index}: {option.get("display")}')
        index += 1    
        continue
      
      print(f'{index}: {option.get("id")}')
      index += 1    

    group_index = self.get_group_index(group_options= group_options, cloud_share= cloud_share)
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "group": {
          "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= (len(group_options) - 1),
          "messages":{
            "validation": f"Valid options are: 0 - {len(group_options) - 1}",
          },
          "conversion": lambda item: self.get_common().helper_type().int().get(item),
          "desc": f"Please select the tenant to use \nValid Options: 0 - {len(group_options) - 1}",
          "default": group_index,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": group_index is not None
        },
      }
    )

    if(response is not None):
      if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= response.get("group").get("formated")):
        self.get_cloud_share_config_value(
          config_key= cloud_share
        )["group"] = group_options[response.get("group").get("formated")].get("id") if response.get("group").get("formated") > 0 else ""
        self._save_config_cloud_share()

        print("-----------------------------")
        print()
        print(f"Group Updated: {self.get_cloud_share_config_value(config_key= cloud_share).get('group')}")
        print()
        print("-----------------------------")

        return
      
    
    print("-----------------------------")
    print()
    print(f"Group NOT Updated")
    print()
    print("-----------------------------")

  

  
  def get_drive_item_index(self, drive_item_id_options, position, cloud_share):
    try:
      index = 0
      drive_id = None
      if self.get_cloud_share_config_value(config_key= cloud_share).get("drive_id") is not None:
        drive_id = self.get_cloud_share_config_value(config_key= cloud_share).get('drive_id')[position]
      if drive_id is None:
        return drive_id
      
      for drive_item in drive_item_id_options:
        if drive_item.get("id") == drive_id:
          return index
        index += 1
    except:
      pass

    return None
  
  def get_drive_item_location_options(self, ms_graph, drive_item_id, cloud_share):
    location_options_base = []
    remove_entry = {
      "id": "Remove Entry",
      "display": "Remove Entry (does not remove it from ms365)"
    }
      
    new_folder = {
      "id": "New Folder",
      "display": "New Folder"
    }
      
    select = {
      "id": "Select",
      "display": "Select"
    }

    if self.get_cloud_share_config_value(config_key= cloud_share).get('group') and drive_item_id == "root":
      location_options_base.append(select)
      location_options_base.append(new_folder)
    
    if drive_item_id != "root":
      location_options_base.append(select)
      location_options_base.append(new_folder)
      location_options_base.append(remove_entry)
    
    base_path = "me" if self.get_cloud_share_config_value(config_key= cloud_share).get('group') == "@me" else f"groups/{self.get_cloud_share_config_value(config_key= cloud_share).get('group')}"
    local_drive_options = ms_graph.send_request(
      url = ms_graph.generate_graph_url(resource= "me", base_path= f"{base_path}/drive/items/{drive_item_id}/children")
    )
    return location_options_base + [
      {"id": drive_option.get("id"), "display": f"{drive_option.get('id')} - {drive_option.get('displayName')}"} for drive_option in local_drive_options.get("value") if drive_option.get("file") is None and drive_option.get("folder") is not None
    ]
  
  def _step_ms365_tenant_path(self, cloud_share, data_client, *args, **kwargs):

    print("-----------------------------")
    print()
    print("What folder will the CMDB be stored in")
    print()
    print("-----------------------------")
    
    
    index = 1
    print("loading groups")




    
    ms_graph = self.get_common().graph().graph(graph_method= "msgraph", credentials= data_client.get_cloud_client().get_tenant_credential(tenant= self.get_cloud_share_config_value(config_key= cloud_share).get('tenant_id')))
    
    drive_item_ids = [
      {"id": "root", "display": "root"}
    ]
    drive_item_position = 0
    drive_item_id_options = []
    drive_id_selected = False
    while not drive_id_selected:

      drive_item_id_options.append(self.get_drive_item_location_options(ms_graph= ms_graph, drive_item_id= drive_item_ids[drive_item_position]['id']))

      print("-----------------------------")
      print(f"Folders in {drive_item_ids[drive_item_position].get('display')}")
      print("-----------------------------")
      
      index = 0
      for option in drive_item_id_options[drive_item_position]:
        print(f'{index}: {option.get("display")}')
        index += 1   

      drive_item_index = self.get_drive_item_index(drive_item_id_options= drive_item_id_options[drive_item_position], cloud_share= cloud_share)
      response = self.get_common().generate_data().generate(
        generate_data_config = {
          "drive_id": {
            "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item) and self.get_common().helper_type().general().is_integer(item) and self.get_common().helper_type().int().get(item) >= 0 and self.get_common().helper_type().int().get(item) <= (len(drive_item_id_options[drive_item_position]) - 1),
            "messages":{
              "validation": f"Valid options are: 0 - {len(drive_item_id_options[drive_item_position]) - 1}",
            },
            "conversion": lambda item: self.get_common().helper_type().int().get(item),
            "desc": f"Please select the tenant to use \nValid Options: 0 - {len(drive_item_id_options[drive_item_position]) - 1}",
            "default": drive_item_index,
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": drive_item_index is not None
          },
        }
      )

      if response is None:
        print("-----------------------------")
        print()
        print(f"Drive ID NOT Updated")
        print()
        print("-----------------------------")
        return

    # if(response is not None):
    #   if not self.get_common().helper_type().string().is_null_or_whitespace(string_value= response.get("group").get("formated")):
    #     self.get_cloud_share_config_value(
    #       config_key= cloud_share
    #     )["group"] = group_options[response.get("group").get("formated")].get("id") if response.get("group").get("formated") > 0 else ""
    #     self._save_config_cloud_share()

    #     print("-----------------------------")
    #     print()
    #     print(f"Group Updated: {self.get_cloud_share_config_value(config_key= cloud_share).get('group')}")
    #     print()
    #     print("-----------------------------")

    #     return
      
    
    print("-----------------------------")
    print()
    print(f"Group NOT Updated")
    print()
    print("-----------------------------")

    
  
    
  
