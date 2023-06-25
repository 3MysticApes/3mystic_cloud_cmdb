from threemystic_cloud_cmdb.cloud_providers.general.cmdb_connector.base_class.base import cloud_cmdb_general_cmdb_connector_base as base
import urllib

class cloud_cmdb_general_cmdb_connector_ms365(base):
  def __init__(self, *args, **kwargs):
    super().__init__(logger_name= "cloud_cmdb_general_cmdb_connector_ms365", *args, **kwargs)
  

  
  def get_cloud_share(self, *args, **kwargs):
    return "ms365"
  
  def _validate_cmdb_init(self, *args, **kwargs):
    self._validate_cmdb_file()

  def _get_ms_graph_drive_id(self, *args, **kwargs):
    if hasattr(self, "_ms365_graph_drive_id"):
      return self._ms365_graph_drive_id
    
    self._ms365_graph_drive_id = self.get_cloud_share_config_value(
      config_key= self.get_cloud_share()
    )["drive_id"]
    return self._get_ms_graph_drive_id(*args, **kwargs)

  def _get_ms_graph_resource_id(self, *args, **kwargs):
    if hasattr(self, "_ms365_graph_resource_id"):
      return self._ms365_graph_resource_id
    
    self._ms365_graph_resource_id = self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group') if self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group') != "me" else None
    return self._get_ms_graph_resource_id(*args, **kwargs)

  def _get_ms_graph_resource(self, *args, **kwargs):
    if hasattr(self, "_ms365_graph_resource"):
      return self._ms365_graph_resource
    
    self._ms365_graph_resource = "me" if self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group') == "me" else f"groups"
    return self._get_ms_graph_resource(*args, **kwargs)

  def _get_ms_graph(self, *args, **kwargs):
    if hasattr(self, "_ms365_graph"):
      return self._ms365_graph
    
    self._ms365_graph = self.get_common().graph().graph(graph_method= "msgraph", 
      credentials= self.get_cloud_client().get_tenant_credential(
        tenant= self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('tenant_id')))
    
    return self._get_ms_graph(*args, **kwargs)
   
  def get_cmdb_file(self, *args, **kwargs):
    if not hasattr(self, "_ms36_cmdb_file"):
      return None
    
    return self._ms36_cmdb_file
  
  def __set_cmdb_file(self, file_details, *args, **kwargs):
    self._ms36_cmdb_file = file_details

  def _validate_cmdb_file(self, *args, **kwargs):

    base_path = f"{self._get_ms_graph_drive_id()[-1].get('id')}" if self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group') == "me" else f"items/{self._get_ms_graph_drive_id()[-1].get('id')}"
    local_drive_options = self._get_ms_graph().send_request(
      url = self._get_ms_graph().generate_graph_url(
        resource= self._get_ms_graph_resource(), 
        resource_id= self._get_ms_graph_resource_id(), 
        base_path= f"drive/{base_path}/children")
    )
    for item in local_drive_options:
      if item.get("file") is not None:
        continue
      if item.get("name") != self.get_cmdb_name():
        continue

      self.__set_cmdb_file(file_details= item)

    if self.get_cmdb_file() is not None:
      return
    
    self._create_cmdb_file()
    self._validate_cmdb_file()

  def _create_cmdb_file(self, *args, **kwargs):
    
    from tempfile import NamedTemporaryFile
    from openpyxl import Workbook
    
    excel_doc = Workbook()
    while len(excel_doc.sheetnames) > 0:
      excel_doc.remove(excel_doc[excel_doc.sheetnames[0]])

    for container in self.get_cmdb_data_containers():
      excel_sheet = excel_doc.create_sheet(container)
      excel_sheet.append(
        self._get_prefix_column() +
        [ column for column in self.get_cmdb_data_containers_columns().get(container) ] +
        self._get_postfix_column()
      )
      excel_sheet.freeze_panes = "A2"
    
    
    with NamedTemporaryFile() as tmp:

      excel_doc.save(tmp.name)
      tmp.seek(0)
    
      base_path = f"{self._get_ms_graph_drive_id()[-1].get('id')}" if self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group') == "me" else f"items/{self._get_ms_graph_drive_id()[-1].get('id')}"
      self._get_ms_graph().send_request(
        url = self._get_ms_graph().generate_graph_url(
          resource= self._get_ms_graph_resource(), 
          resource_id= self._get_ms_graph_resource_id(), 
          base_path= f"drive/{base_path}:/{urllib.parse.quote(self.get_cmdb_name())}:/content"),
          data = tmp.read(),
          params= {"@microsoft.graph.conflictBehavior": "replace"},
          headers= {"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
          method= "put"
      )
  
  def _get_worksheet_data(self, *args, **kwargs):
    if hasattr(self, "_worksheet_data"):
      return self._worksheet_data
    
    return None

  def _validate_workbook_worksheets(self, *args, **kwargs):

    base_path = f"{self.get_cmdb_file().get('id')}" if self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group') == "me" else f"items/{self.get_cmdb_file().get('id')}"
    worksheets_response = self._get_ms_graph().send_request(
      url = self._get_ms_graph().generate_graph_url(
        resource= self._get_ms_graph_resource(), 
        resource_id= self._get_ms_graph_resource_id(), 
        base_path= f"drive/{base_path}/workbook/worksheets"),
        session_config = {
          "type":"workbook",
          "drive_id": self.get_cmdb_file().get('id'),
          "persist_changes": True,
          "group_id": self.get_cloud_share_config_value(config_key= self.get_cloud_share()).get('group')
        },
        method= "get"
    )

    self._worksheet_data = None
    if worksheets_response.get("value") is None:
      return
    
    if len(worksheets_response.get("value")) < 1:
      return
    
    self._worksheet_data = {self.get_common().helper_type().string().set_case(string_value= worksheet["name"], case= "lower"):worksheet for worksheet in worksheets_response["value"]}
    




    
    
  
