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
    
    if cloud_share == "ms365":
      self._step_ms365()
      return
  
  def _step_ms365(self,*args, **kwargs):
    from threemystic_cloud_data_client.cloud_data_client import cloud_data_client
    cloud_data_client = cloud_data_client(
      provider= "azure",
      logger= self.get_logger(), 
      common= self.get_common()
    )
  
    
  
