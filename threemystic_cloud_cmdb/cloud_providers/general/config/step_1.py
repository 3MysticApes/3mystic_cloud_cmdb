from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers



class cloud_cmdb_general_config_step_1(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_1", *args, **kwargs)
    

  def step(self, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "default_provider": {
            "validation": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower") in self.get_supported_providers(),
            "messages":{
              "validation": f"Valid options are: {self.get_supported_providers()}",
            },
            "conversion": lambda item: self.get_common().helper_type().string().set_case(string_value= item, case= "lower"),
            "desc": f"What is the default provider? If empty or blank you will be required to pass in a provider with every call.\nValid Options: {self.get_supported_providers()}",
            "default": self.get_default_provider(),
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": not self.get_common().helper_type().string().is_null_or_whitespace(string_value= self.get_default_provider())
        }
      }
    )

    if(response is not None):
      for key, item in response.items():
        self._update_config(config_key= key, config_value= item.get("formated"))
      self._save_config()
      print("-----------------------------")
      print()
      print()
      print("Base Configuration is updated")
      print()
      print()
      print("-----------------------------")

    
    
  
