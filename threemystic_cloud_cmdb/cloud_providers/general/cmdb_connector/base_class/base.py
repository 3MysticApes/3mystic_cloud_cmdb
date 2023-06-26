from threemystic_cloud_cmdb.cloud_providers.base_class.base import cloud_cmdb_provider_base as base
from abc import abstractmethod

class cloud_cmdb_general_cmdb_connector_base(base):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__set_cloud_client(*args, **kwargs)
    self.__set_cmdb_data_containers(*args, **kwargs)
    self.__set_cmdb_data_containers_columns(*args, **kwargs)
    self.__set_cmdb_postfix_columns(*args, **kwargs)

    if(self.has_cloud_share_configured()):
      self._validate_cmdb_init()


  @abstractmethod
  def get_cloud_share(self, *args, **kwargs):
    pass

  @abstractmethod
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
    if self._cmdb_postfix_column_settings.get("delete"):
      self._cmdb_postfix_columns.append("DELETED")
    if self._cmdb_postfix_column_settings.get("empty"):
      self._cmdb_postfix_columns.append("")

    return self._get_postfix_column(*args, **kwargs)

  def __set_cmdb_postfix_columns(self, auto_load = None, data_container_settings = None, *args, **kwargs):
    if auto_load is not None:   
      if hasattr(auto_load, "_cmdb_postfix_column_settings"):
        return self.__set_cmdb_postfix_columns(data_container_settings= auto_load._cmdb_postfix_column_settings)
    
    self._cmdb_postfix_column_settings = {}
    if data_container_settings is None:
      data_container_settings = {}
    for data_container in self.get_cmdb_data_containers():
      self._cmdb_postfix_column_settings[data_container] = self.get_common().helper_type().dictionary().merge_dictionary([
        {},
        data_container_settings.get(data_container) if data_container_settings.get(data_container) is not None else {},
        {
          "delete": True,
          "empty": True,
        }
      ])

      
    data_container_settings
    

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
  
  def __set_cloud_client(self, auto_load = None, cloud_client = None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cloud_client() is not None:
        return self.__set_cloud_client(cloud_client= auto_load.get_cloud_client())

    self.__cmdb_cloud_client = cloud_client

  def get_cmdb_data_containers(self, *args, **kwargs):
    return self.__cmdb_data_containers
  
  def __set_cmdb_data_containers(self, auto_load = None, data_containers = None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cmdb_data_containers() is not None:
        return self.__set_cmdb_data_containers(data_containers= auto_load.get_cmdb_data_containers())

    self.__cmdb_data_containers = data_containers

  def get_cmdb_data_containers_columns(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns"):
      return self._cmdb_data_containers_columns

    self._cmdb_data_containers_columns = {}
    for key, columns in self.__cmdb_data_containers_columns_raw.items():
      self._cmdb_data_containers_columns[key] = (self._get_prefix_column() +
        columns +
        self._get_postfix_column())
    
    return self.get_cmdb_data_containers_columns()
  
  def __set_cmdb_data_containers_columns(self, auto_load= None, container_columns= None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cmdb_data_containers() is not None:
        return self.__set_cmdb_data_containers_columns(container_columns= auto_load.get_cmdb_data_containers_columns())

    self.__cmdb_data_containers_columns_raw = container_columns
    
  
