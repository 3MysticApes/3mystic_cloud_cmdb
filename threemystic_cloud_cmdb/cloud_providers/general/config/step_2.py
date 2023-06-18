from threemystic_cloud_cmdb.cloud_providers.general.config.base_class.base import cloud_cmdb_general_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers



class cloud_cmdb_general_config_step_2(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_config_step_1", *args, **kwargs)
    

  def step(self, *args, **kwargs):
    if not super().step(run_base_config= True):
      return
    
    response = self.get_common().generate_data().generate(
      generate_data_config = {
        "default_cmdb_report_path": {
            "validation": lambda item: self.get_common().helper_type().path().is_valid_filepath(path= item),
            "messages":{
              "validation": f"A valid path is required",
            },
            "conversion": lambda item: item,
            "desc": f"Where should the reports be saved locally?",
            "default": self.default_report_path(),
            "handler": generate_data_handlers.get_handler(handler= "base"),
            "optional": True
        }
      }
    )

    if(response is not None):
      for key, item in response.items():
        self._update_cmdb_config(config_key= key, config_value= item.get("formated"))
      self._save_config()
      print("-----------------------------")
      print()
      print()
      print("Base Configuration is updated")
      print()
      print()
      print("-----------------------------")
    else:
      print("-----------------------------")
      print()
      print()
      print("Base Configuration NOT updated")
      print()
      print()
      print("-----------------------------")

    
    
  
