from threemystic_common.base_class.base_provider import base
import textwrap, argparse

class cloud_cmdb_provider_base_cmdb(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self._set_max_process_pool(*args, **kwargs)
    self._set_max_thread_pool(*args, **kwargs)
    self._set_data_start(*args, **kwargs)

  def get_data_start(self, *args, **kwargs):
    return self.__data_start
  
  def _set_data_start(self, *args, **kwargs):
    self.__data_start = self.get_common().helper_type().datetime().get()

  def get_max_process_pool(self, *args, **kwargs):
    return self._max_process_pool
  
  def _set_max_process_pool(self, max_thread_pool = 5, *args, **kwargs):
    self._max_process_pool = max_thread_pool

  def get_max_thread_pool(self, *args, **kwargs):
    return self._max_thread_pool
  
  def _set_max_thread_pool(self, max_thread_pool = 35, *args, **kwargs):
    self._max_thread_pool = max_thread_pool

  async def _pre_load_main_process(self, *args, **kwargs):
    pass
   