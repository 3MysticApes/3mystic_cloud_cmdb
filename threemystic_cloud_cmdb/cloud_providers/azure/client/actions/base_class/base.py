from threemystic_cloud_cmdb.cloud_providers.base_class.base_cmdb import cloud_cmdb_provider_base_cmdb as base

class cloud_cmdb_azure_client_action_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(provider= "azure", *args, **kwargs)  
    