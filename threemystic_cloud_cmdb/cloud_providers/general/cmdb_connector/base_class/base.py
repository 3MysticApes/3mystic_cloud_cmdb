from threemystic_cloud_cmdb.cloud_providers.base_class.base import cloud_cmdb_provider_base as base
import abc

class cloud_cmdb_general_cmdb_connector_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__set_cloud_client(*args, **kwargs)
    self.__set_cmdb_data_containers(*args, **kwargs)
    self.__set_cmdb_data_containers_columns(*args, **kwargs)
    self.__set_cmdb_postfix_columns(*args, **kwargs)


  @abc.abstractclassmethod
  def get_cloud_share(self, *args, **kwargs):
    pass

  @abc.abstractclassmethod
  def _validate_cmdb_init(self, *args, **kwargs):
    pass
  
  def _get_prefix_column(self, *args, **kwargs):    
    if hasattr(self, "_cmdb_prefix_columns"):
      return self._cmdb_prefix_columns
    
    self._cmdb_prefix_columns = ["Source"]
    return self._get_prefix_column(*args, **kwargs)
  
  def _get_postfix_column(self, *args, **kwargs):    
    if hasattr(self, "_cmdb_postfix_columns"):
      return self._cmdb_postfix_columns
    
    self._cmdb_postfix_columns = []
    if self.__cmdb_postfix_column_settings.get("delete"):
      self._cmdb_postfix_columns.append("DELETED")
    if self.__cmdb_postfix_column_settings.get("empty"):
      self._cmdb_postfix_columns.append("")

    return self._get_postfix_column(*args, **kwargs)

  def __set_cmdb_postfix_columns(self, include_delete_column, include_empty_column, *args, **kwargs):
    self.__cmdb_postfix_column_settings = {
      "delete": include_delete_column,
      "empty": include_empty_column,
    }

  def get_cmdb_name(self, *args, **kwargs):
    if hasattr(self, "_cmdb_name"):
      return self._cmdb_name
    
    self._cmdb_name = self.get_common().helper_type().string().set_case(
      string_value= self.get_cloud_share_config_value(config_key= "name"),
      case= "lower"
    )
    
    return self.get_cmdb_name(*args, **kwargs)
  
  def get_cloud_client(self, *args, **kwargs):
    return self.__cmdb_cloud_client
  
  def __set_cloud_client(self, cloud_client, *args, **kwargs):
    self.__cmdb_cloud_client = cloud_client

  def get_cmdb_data_containers(self, *args, **kwargs):
    return self.__cmdb_data_containers
  
  def __set_cmdb_data_containers(self, data_containers, *args, **kwargs):
    self.__cmdb_data_containers = data_containers

  def get_cmdb_data_containers_columns(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns"):
      return self._cmdb_data_containers_columns

    self._cmdb_data_containers_columns = {}
    for key, columns in self.get_cmdb_data_containers_columns().items():
      self._cmdb_data_containers_columns[key] = (self._get_prefix_column() +
        columns +
        self._get_postfix_column())
    
    return self.get_cmdb_data_containers_columns()
  
  def __set_cmdb_data_containers_columns(self, container_columns, *args, **kwargs):
    self.__cmdb_data_containers_columns_raw = container_columns
    
  
