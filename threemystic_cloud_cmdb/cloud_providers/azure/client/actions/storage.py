from threemystic_cloud_cmdb.cloud_providers.azure.client.actions.base_class.base import cloud_cmdb_azure_client_action_base as base
import asyncio

class cloud_cmdb_azure_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="storage", 
      logger_name= "cloud_cmdb_azure_client_action_storage", 
      uniqueid_lambda = lambda: True
      *args, **kwargs)
  
  def main(self, *args, **kwargs):

    print("storage")
    

  async def _process_account_data(self, account, loop, *args, **kwargs):

    print("storage")