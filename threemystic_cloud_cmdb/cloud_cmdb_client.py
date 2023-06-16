from threemystic_cloud_cmdb.cloud_providers.base_class.base import cloud_cmdb_provider_base as base

class cloud_cmdb_client(base): 
  """This is a library to help with the interaction with the cloud providers"""

  def __init__(self, logger = None, common = None, *args, **kwargs) -> None: 
    super().__init__(provider= "", common= common, logger_name= "cloud_cmdb_client", logger= logger, *args, **kwargs)
    
  def version(self, *args, **kwargs):
    if hasattr(self, "_version"):
      return self._version
    import threemystic_cloud_cmdb.__version__ as __version__
    self._version = __version__.__version__
    return self.version()
    
  def get_supported_providers(self, *args, **kwargs):
    return super().get_supported_providers()
  
  def init_client(self, provider, *args, **kwargs):
    pass

  def client(self, provider = None, *args, **kwargs):
    return None

  