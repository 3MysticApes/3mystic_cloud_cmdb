from threemystic_cloud_cmdb.cloud_providers.azure.config.base_class.base import cloud_cmdb_azure_config_base as base
from threemystic_common.base_class.generate_data.generate_data_handlers import generate_data_handlers
from threemystic_cloud_data_client.cloud_data_client import cloud_data_client as data_client
from threemystic_cloud_data_client.cli.actions.config import cloud_data_client_config as user_action
from threemystic_cloud_cmdb.cloud_providers.general  import cloud_cmdb_general as cmdb_client


class cloud_cmdb_azure_config_step_1(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_azure_config_step_1", *args, **kwargs)
    
  def check_cloud_data_client(self, *args, **kwargs):
    client = data_client( common= self.get_common())

    if client.is_general_config_completed() and client.is_config_completed():
      print()
      print()
      print("--------------------------------------------------------------")
      print(f"The data general config has been configured, do you want to update?")
      response = self.get_common().generate_data().generate(
        generate_data_config = {
          "base_config": {
            "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
            "messages":{
              "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
            },
            "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
            "desc": f"Do you want to update the Cloud Data Client.\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
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
    
    user_action(cloud_client= client).main(
      provider= "azure",
      *args, **kwargs
    )

  def check_cloud_general(self, *args, **kwargs):
    client = cmdb_client( 
      common= self.get_common(),
      provider= "azure"
    )

    if self.is_general_config_completed():
      print()
      print()
      print("--------------------------------------------------------------")
      print(f"The cmdb general config has been configured, do you want to update?")
      response = self.get_common().generate_data().generate(
        generate_data_config = {
          "base_config": {
            "validation": lambda item: self.get_common().helper_type().bool().is_bool(check_value= item),
            "messages":{
              "validation": f"Valid options for Yes are: {self.get_common().helper_type().bool().is_true_values()}",
            },
            "conversion": lambda item: self.get_common().helper_type().bool().is_true(check_value= item),
            "desc": f"CMDB Client: Do you want to update base config?\nLeave blank to exit.\nValid Options: {self.get_common().helper_type().bool().is_true_values()}",
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
    
    if not self.is_general_config_completed():
      print("You must configure the CMDB General Config...")
      self.get_common().helper_type().datetime().time_sleep(seconds= 2)
    client.action_config()

  def step(self, *args, **kwargs):
    
    self.check_cloud_data_client(*args, **kwargs)    
    self.check_cloud_general(*args, **kwargs)

    print()
    print()
    print()
    print(f"No additional config is required at this time for Data Client: {self.get_provider()}")
    
    
  
