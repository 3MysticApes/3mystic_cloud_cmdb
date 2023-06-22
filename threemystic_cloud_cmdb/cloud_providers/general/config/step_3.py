from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers



class cloud_cmdb_general_config_step_2(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_1", *args, **kwargs)
    
  def step_tag_question(self, *args, **kwargs):
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "name": {
            "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item),
            "messages":{
              "validation": f"The tag cannot be blank, please use quit/exit to end.",
            },
            "conversion": lambda item: item,
            "desc": f"The name of the tag?",
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": False
        },
        "alt_names": {
            "validation": lambda item: not self.get_common().helper_type().string().is_null_or_whitespace(string_value= item),
            "messages":{
              "validation": f"The tag cannot be blank, please use quit/exit to end.",
            },
            "conversion": lambda item: item,
            "desc": f"Alternative Names for the tag",
            "default": None,
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": True
        }
      }
    )

  def step(self, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    
    print("-----------------------------")
    print()
    print()
    print("CMDB Cloud Share")
    print()
    print()
    print("-----------------------------")
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "track_custom_tags": {
          "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
          "messages":{
            "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
          },
          "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
          "desc": f"Do you want to track Custom Tags as part of the CMDB?\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
          "default": None,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": True
        }
      }
    )

    if response is None:
      return
    if not self.get_common().helper_type().bool().is_true(check_value= response.get("base_config").get("formated")):
      return

    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "track_custom_tags": {
          "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
          "messages":{
            "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
          },
          "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
          "desc": f"Do you want to edit the existing tags?\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
          "default": None,
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": True
        }
      }
    )
    replace_existing_tags = True
    if response is None:
      return
    if not self.get_common().helper_type().bool().is_true(check_value= response.get("track_custom_tags").get("formated")):
      return

    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "cloud_share_location": {
          "validation": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower") in self.get_supported_cloud_share(),
          "messages":{
            "validation": f"Valid options are: {self.get_supported_cloud_share()}",
          },
          "conversion": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower"),
          "desc": f"What is the cloud share you would like to use? \nValid Options: {self.get_supported_cloud_share()}",
          "default": self.get_cloud_share_config_value(
            config_key= "cloud_share_location"
          ),
          "handler": generate_data_handlers.get_handler(handler= "base"),
          "optional": not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_cloud_share_config_value(
            config_key= "cloud_share_location"
          ))
        },
      }
    )

    if(response is not None):
      for key, item in response.items():
        self._update_config_cloud_share(config_key= key, config_value= item.get("formated"))
      self._save_config_cloud_share()

      from threemystic_cloud_cmdb.cloud_providers.general.config.step_2_cloud_share import cloud_cmdb_general_config_step_2_cloud_share as step
      next_step = step(common= self.get_common(), logger= self.get_logger())
      
      next_step.step(cloud_share= self.get_cloud_share_config_value(config_key= "cloud_share_location"))

      print("-----------------------------")
      print()
      print()
      print("CMDB Cloud Share is updated")
      print()
      print()
      print("-----------------------------")
    else:
      print("-----------------------------")
      print()
      print()
      print("CMDB Cloud Share NOT updated")
      print()
      print()
      print("-----------------------------")

    
    
  
