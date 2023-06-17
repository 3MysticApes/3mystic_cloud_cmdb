from threemystic_common.base_class.base_provider import base
from threemystic_common.base_class.base_script_options import base_process_options

import textwrap, argparse
import asyncio, concurrent.futures

class cloud_cmdb_provider_base_client(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__set_cloud_cmdb(*args, **kwargs)
    self.__set_cloud_data_client(*args, **kwargs)
    
    self._default_parser_init = {
      "prog": f'3mystic_cloud_cmdb -g -p {kwargs["provider"]}',
      "formatter_class": argparse.RawDescriptionHelpFormatter,
      "description": textwrap.dedent('''\
      Requires additional settings.
        One data Action (if more than one is selected only the last one will be ran)
      '''),
      "add_help": False,
      "epilog": ""
    }

    self._set_action_from_arguments(*args, **kwargs)

    self._set_data_action()
  
  def get_default_parser_args(self, *args, **kwargs):
    if hasattr(self, "_cmdb_default_parser_args"):
      return self._cmdb_default_parser_args
    
    from threemystic_cloud_data_client.cloud_providers.base_class.base_client import cloud_data_client_provider_base_client
    self._cmdb_default_parser_args = self.get_common().helper_type().dictionary().merge_dictionary([
      {
        "--all, -a": {
          "default": None, 
          "const": "all",
          "dest": "data_action",
          "help": "Data Action: This will generate cmdb for all supported reports.",
          "action": 'store_const'
        }
      },      
      cloud_data_client_provider_base_client.get_default_parser_args(),
    ])
    return self.get_default_parser_args()

  def __get_action_parser_options(self, *args, **kwargs):
    if hasattr(self, "_action_process_options"):
      return self._action_process_options
    
    self._action_process_options = base_process_options(common= self.get_common())
    return self.__get_action_parser_options()
    
  def _get_action_parser(self, *args, **kwargs):
    if hasattr(self, "_action_parser"):
      return self._action_parser
    
    
    self._action_parser = self.__get_action_parser_options().get_parser(
      parser_init_kwargs = self._default_parser_init,
      parser_args = self.get_common().helper_type().dictionary().merge_dictionary([
         self.get_default_parser_args(),
      ])
    )
    return self._get_action_parser()
  
  def get_action_from_arguments(self, *args, **kwargs):
    if hasattr(self, "_action_from_arguments"):
      return self._action_from_arguments
    
    return {}
  
  def _set_action_from_arguments(self, force_action_arguments = None, *args, **kwargs):
    if force_action_arguments is not None:
      self._action_from_arguments = force_action_arguments
      return self.get_action_from_arguments()

    processed_info = self.__get_action_parser_options().process_opts(
      parser = self._get_action_parser()
    )

    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= processed_info["processed_data"].get("data_action")):
      self._get_action_parser().print_help()
      return None
    
    self._action_from_arguments = processed_info["processed_data"]
    return self.get_action_from_arguments()  
  

  def run(self, *args, **kwargs):
    if self.get_data_action() is None:
      return
    
    asyncio.run(self.get_data_action().main())

  def _set_data_action(self, *args, **kwargs):
    if self.get_action_from_arguments() is None or len(self.get_action_from_arguments()) < 1:
      return

    try:
      self._data_action_data = self._process_data_action(
        provider = self.get_provider(),
        action= self.get_common().helper_type().string().set_case(string_value= self.get_action_from_arguments().get('data_action') , case= "lower"), 
        *args, **kwargs)
      
    except Exception as err:
      print(f"The action {self.get_action_from_arguments().get('data_action')} is unknown")
      self.get_common().get_logger().exception(f"The action {self.get_action_from_arguments() .get('data_action')} is unknown", extra={"exception": err})
      self._get_action_parser().print_help()
  
  def _process_data_action(self, provider, action, *args, **kwargs):    
    if self.get_common().helper_type().string().is_null_or_whitespace(string_value= action):
      return None
    data_action = __import__(f'threemystic_cloud_cmdb.cloud_providers.{provider}.client.actions.{action}', fromlist=[f'cloud_cmdb_{provider}_client_action'])
    process_data_action = getattr(data_action, f'cloud_cmdb_{provider}_client_action')(
      cloud_data_client= self,
      common= self.get_common(),
      logger= self.get_common().get_logger()
    )
    return process_data_action
  
  def get_data_action(self, *args, **kwargs):
    if hasattr(self, "_data_action_data"):
      return self._data_action_data
    
    return None
  
  async def process_multiple_data_actions(self, provider, actions, *args, **kwargs):
    if actions == "all":
      actions = [self.get_common().helper_type().string().set_case(string_value= action["const"]) for action in self.get_default_parser_args() if self.get_common().helper_type().string().set_case(string_value= action["const"])]
    
    running_tasks = []
    with concurrent.futures.ThreadPoolExecutor(self.get_max_thread_pool()) as pool:
      for action in actions:
        if self.get_common().helper_type().string().set_case(string_value= action) == "all":
          continue
        process_data_action = self.process_data_action(provider= provider, action= action, *args, **kwargs)
        running_tasks = asyncio.get_event_loop().create_task(process_data_action.main(pool= pool))
      
      await asyncio.wait(running_tasks)
  
  def get_cloud_cmdb(self, *args, **kwargs):
    return self.__cloud_cmdb
  
  def __set_cloud_cmdb(self, cloud_cmdb, *args, **kwargs):
    self.__cloud_cmdb = cloud_cmdb
  
  def get_cloud_data_client(self, *args, **kwargs):
    return self.__get_cloud_data_client_raw().client(
      force_action_arguments= self.get_action_from_arguments(),
      suppress_parser_help= True,
    )
  
  def __get_cloud_data_client_raw(self, *args, **kwargs):
    return self.__cloud_data_client_raw
  
  def __set_cloud_data_client(self, cloud_data_client, *args, **kwargs):
    self.__cloud_data_client_raw = cloud_data_client
    
  
  def get_cloud_client(self, *args, **kwargs):
    return self.get_cloud_data_client().get_cloud_client()

  
  
    

  
  

