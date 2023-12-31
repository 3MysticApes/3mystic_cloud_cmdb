import sys
from threemystic_common.base_class.base_script_options import base_process_options
from threemystic_cloud_data_client.cloud_data_client import cloud_data_client
from threemystic_cloud_client.cloud_client import cloud_client


class cloud_cmdb_cli(base_process_options):
  def __init__(self, *args, **kwargs):
    from threemystic_cloud_cmdb.cloud_cmdb_client import cloud_cmdb_client
    self._cloud_cmdb_client = cloud_cmdb_client()
    
    super().__init__(common= self._cloud_cmdb_client.get_common(), *args, **kwargs)

    self.parser = self.get_parser(
      parser_init_kwargs = {
        "description": "One Action is required"
      },
      parser_args = {
        # I can create other actions just by duplication this and changing the const,
        "--version": {
            "default": None, 
            "const": "version",
            "dest": "client_action",
            "help": "Action: outputs the versions of the app being used.",
            "action": 'store_const'
        },
        "--config,-c": {
            "default": None, 
            "const": "config",
            "dest": "client_action",
            "help": "Action: This is so you can setup the data client",
            "action": 'store_const'
        },
        "--generate,-g": {
            "default": None, 
            "const": "generate",
            "dest": "client_action",
            "help": "Action: Generate the CMDB. (must also select the data to run or --all to generate for all)",
            "action": 'store_const'
        },
        "--provider,-p": {
            "default": None, 
            "type": str,
            "choices": self._cloud_cmdb_client.get_supported_providers(),
            "dest": "client_provider",
            "help": "Provider: This is to set the provider that should be used",
            "action": 'store'
        },
      }
    )

    processed_info = self.process_opts(
      parser = self.parser
    )

    for key, value in processed_info["processed_data"].items():
      setattr(self, f"_{key}", value)
    
    
  def process_client_action(self, force_action = None, *args, **kwargs):
    if self._cloud_cmdb_client.get_common().helper_type().string().is_null_or_whitespace(string_value= force_action):
      force_action = self.__get_client_acount()
    if force_action == "version":
      self.version_dispaly()
      return

    if force_action == "config":
      if not "provider" in kwargs:
        if not self._cloud_cmdb_client.get_common().helper_type().string().is_null_or_whitespace(string_value= self._client_provider):
          kwargs["provider"] = self._client_provider

      from threemystic_cloud_cmdb.cli.actions.config import cloud_cmdb_config as user_action
      user_action(cloud_cmdb_client= self._cloud_cmdb_client).main(*args, **kwargs)
      return
    
    if force_action == "generate":
      if not "provider" in kwargs:
        if not self._cloud_cmdb_client.get_common().helper_type().string().is_null_or_whitespace(string_value= self._client_provider):
          kwargs["provider"] = self._client_provider
      self._cloud_cmdb_client.client(*args, **kwargs).run()
      return
    


    return      
  

  def version_dispaly(self, *args, **kwargs):
    data_client = cloud_data_client(
      logger= self._cloud_cmdb_client.get_common().get_logger(),
      common= self._cloud_cmdb_client.get_common())
    client = cloud_client(
      logger= self._cloud_cmdb_client.get_common().get_logger(),
      common= self._cloud_cmdb_client.get_common())
    
    print(f"You currenly have installed")    
    print(f"3mystic_cloud_cmdb: v{self._cloud_cmdb_client.version()}")
    print(f"3mystic_cloud_data_client: v{data_client.version()}")
    print(f"3mystic_cloud_client: v{client.version()}")
    print(f"3mystic_common: v{self._cloud_cmdb_client.get_common().version()}")
    print()
    print(f"Current supported cloud providers: {self._cloud_cmdb_client.get_supported_providers()}")
    print(f"Cloud Providers config status: ")
    
    print(f"CMDB Client General Configuration: {self._cloud_cmdb_client.is_general_config_completed()}")
    print()

    print(f"3mystic_cloud_data_client General Configuration: {data_client.client(provider= self._cloud_cmdb_client.get_supported_providers()[0], suppress_parser_help= True).get_cloud_data_client().is_general_config_completed()}")
    print()
    for cloud_provider in client.get_supported_providers():
      provider_data_client = data_client.client(provider= cloud_provider, suppress_parser_help= True)
      
      print()
      print(f"{cloud_provider}: ")
      print(f"cmdb client: {self._cloud_cmdb_client.client(provider= cloud_provider, suppress_parser_help= True).get_cloud_cmdb().is_config_completed()}")
      print(f"3mystic_cloud_data_client: {provider_data_client.get_cloud_data_client().is_config_completed()}")
      print(f"3mystic_cloud_client: {provider_data_client.get_cloud_client().is_provider_config_completed() if provider_data_client.get_cloud_client() is not None else False}")


  def __get_client_acount(self, *args, **kwargs):
    if not hasattr(self, "_client_action"):
      return None
    
    return self._client_action
  def main(self, *args, **kwargs):    
    if self.__get_client_acount() is None:
      print(f"Thank you for using the 3 Mystic Apes Cloud Client.")
      self.version_dispaly()
      print()
      self.parser.print_help()
      return
    
    self.process_client_action( )

def main(*args, **kwargs):    
  cloud_cmdb_cli(*args, **kwargs).main(*args, **kwargs)
    

if __name__ == '__main__':   
  cloud_cmdb_cli().main(sys.argv[1:])