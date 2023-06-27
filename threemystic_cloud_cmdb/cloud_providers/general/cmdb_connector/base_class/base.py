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

    self._cmdb_prefix_columns = [{
      "id": "source",
      "display": "Source",
      "handler": lambda item: self.get_cloud_client().get_provider()
    }]
    return self._get_prefix_column(*args, **kwargs)
  
  def _get_postfix_column(self, *args, **kwargs):    
    if hasattr(self, "_cmdb_postfix_columns"):
      return self._cmdb_postfix_columns
    
    self._cmdb_postfix_columns = {}
    for data_container_key, settings in self._cmdb_postfix_column_settings.items():
      self._cmdb_postfix_columns[data_container_key] = []
      if settings.get("include_delete_column"):
        self._cmdb_postfix_columns[data_container_key].append({
          "id": "deleted",
          "display": "DELETED",
          "handler": lambda item: ""
        })
      if settings.get("include_empty_column"):
        self._cmdb_postfix_columns[data_container_key].append({
          "id": "empty",
          "display": "",
          "handler": lambda item: ""
        })


    return self._get_postfix_column(*args, **kwargs)

  def __set_cmdb_postfix_columns(self, *args, **kwargs):
    
    self._cmdb_postfix_column_settings = {}

    for data_container_key, data_container_data in self.get_cmdb_data_containers().items():
      self._cmdb_postfix_column_settings[data_container_key] = self.get_common().helper_type().dictionary().merge_dictionary([
        {},
        {
          "include_delete_column": True,
          "include_empty_column": True,
        },
        data_container_data.get("cmdb_connector") if  data_container_data.get("cmdb_connector") is not None else {},
      ])
    

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

  def get_cmdb_data_containers_column_names(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns_name"):
      return self._cmdb_data_containers_columns_name
    
    return None
  
  def _get_cmdb_data_containers_hidden(self, container, *args, **kwargs):
    if container.get("cmdb") is None:
      return (container.get("hidden") is True)
    
    if container.get("cmdb").get(self.get_cloud_share()) is not None:
      if container.get("cmdb").get(self.get_cloud_share()).get("hidden") is not None:
        return (container.get("cmdb").get(self.get_cloud_share()).get("hidden") is True)
      
    if container.get("cmdb").get("hidden") is not None:
      return (container.get("cmdb").get("hidden") is True)


    return False

  def _get_cmdb_data_containers_display(self, container, *args, **kwargs):
    if container.get("cmdb") is None:
      return (container.get("display"))
    
    if container.get("cmdb").get(self.get_cloud_share()) is not None:
      if "display" in container.get("cmdb").get(self.get_cloud_share()):
        return container.get("cmdb").get(self.get_cloud_share()).get("display")
      
    if "display" in container.get("cmdb"):
      return container.get("cmdb").get("display")


    return container.get("display")


  def _set_cmdb_data_containers_column_names(self, container_name, columns, *args, **kwargs):    
    if not hasattr(self, "_cmdb_data_containers_columns_name"):
      self._cmdb_data_containers_columns_name = {}
    
    self._cmdb_data_containers_columns_name[container_name] = {}
    for column in columns:
  
      if self._get_cmdb_data_containers_hidden(container= column):
        continue

      self._cmdb_data_containers_columns_name[container_name][column["id"]] = {
        "display": self._get_cmdb_data_containers_display(container= column)
      }


  def get_cmdb_data_containers_columns_raw(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns_raw"):
      return self._cmdb_data_containers_columns_raw
    
    self._cmdb_data_containers_columns_raw = {}
    for data_container in self.__cmdb_data_containers_columns_raw.keys():
      self._cmdb_data_containers_columns_raw[data_container] = (
        self._get_prefix_column() +
        [ item for item in self.get_cmdb_data_containers_column_names()[data_container].values()] +
        self._get_postfix_column()[data_container]
      )
    
    return self.get_cmdb_data_containers_columns_raw()
  
  def get_cmdb_data_containers_columns(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_columns"):
      return self._cmdb_data_containers_columns
    
    self._cmdb_data_containers_columns = {}
    for data_container in self.__cmdb_data_containers_columns_raw.keys():
      self._cmdb_data_containers_columns[data_container] = (
        [ self._get_cmdb_data_containers_display(container= item) for item in self.get_cmdb_data_containers_columns_raw() ]
      )
    
    return self.get_cmdb_data_containers_columns()
  
  def __set_cmdb_data_containers_columns(self, auto_load= None, container_columns= None, *args, **kwargs):
    if auto_load is not None:
      if auto_load.get_cmdb_data_containers() is not None:
        return self.__set_cmdb_data_containers_columns(container_columns= auto_load.__cmdb_data_containers_columns_raw)

    self.__cmdb_data_containers_columns_raw = container_columns
    for data_container, columns in self.__cmdb_data_containers_columns_raw.items():
      self._set_cmdb_data_containers_column_names(container_name= data_container, columns= columns)
    
  def get_cmdb_data_containers_key_display(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_key_display"):
      return self._cmdb_data_containers_key_display
    
    self._cmdb_data_containers_key_display = {
      data_container_key:self._get_cmdb_data_containers_display(container= data_container) for data_container_key, data_container in self.get_cmdb_data_containers().items()
    }
    return self.get_cmdb_data_containers_key_display(*args, **kwargs)
  
  def get_cmdb_data_containers_display_key(self, *args, **kwargs):
    if hasattr(self, "_cmdb_data_containers_display_key"):
      return self._cmdb_data_containers_display_key
    
    self._cmdb_data_containers_display_key = {
      data_container_display:data_container_key for data_container_key, data_container_display in self.get_cmdb_data_containers_key_display().items()
    }
    return self.get_cmdb_data_containers_display_key(*args, **kwargs)
