import cfg
import requests

kong_url = cfg.get_default("KONG_URL")

def create_new_service(name, host, port):
  """
    Register a new service into Kong Gateway.
    Paramerters:
    ------------
      name: str
        name of microserivce registered in Kong
      host: int
        IP publich of microservice
      port: int
        port of microservice
    Returns:
    --------
  """
  url = "http://" + kong_url + "/services/"
  payload= {
    'name': name,
    'host': host,
    'port': port
  }
  response = requests.request("POST", url, data=payload)
  return response

def create_route_service(name, path):
  """
    Register routes of service in Kong Gateway.
    Paramerters:
    ------------
      name: str
        name of microserivce registered in Kong
      path: str
        path of microservice
    Returns:
    --------
  """
  url = "http://" + kong_url + f"/services/{name}/routes"
  payload={
    'paths': path
  }
  response = requests.request("POST", url, data=payload)
  return response

def get_detail_routes_services(name):
  url = "http://" + kong_url + f"/services/{name}/routes"
  response = requests.request("GET", url)
  return response

def remove_routes(routes_id, name):
  """
    Remove routes of service in Kong Gateway.
    Paramerters:
    ------------
      name: str
        name of microserivce registered in Kong
      routes_id: str
        id of routers
    Returns:
    --------
  """
  url = "http://" + kong_url + f"/services/{name}/routes/{routes_id}"
  response = requests.request("DELETE", url)
  return response

def remove_service(name):
  """
    Remove service of service in Kong Gateway.
    Paramerters:
    ------------
      name: str
        name of microserivce registered in Kong
    Returns:
    --------
  """
  url = "http://" + kong_url + f"/services/{name}/"
  response = requests.request("DELETE", url)
  return response

def proxy_cache(method, status_code, content_type, cache_ttl, strategy):
  """
    Config proxy_cache global for service in Kong.
    Paramerters:
    ------------
      method: str
        HTTP method
      status_code: int
        HTTP status
      content_type: int
        used to indicate the original media type of the resource
      cache_ttl: int
        controls how often user INI files are re-read
      strategy: str
        memory
    Returns:
    --------
  """
  url = "http://" + kong_url + "/plugins"

  payload={
    'name': 'proxy-cache',
    'config.request_method': method,
    'config.response_code': status_code,
    'config.content_type': content_type,
    'config.cache_ttl': cache_ttl,
    'config.strategy': strategy
    }
  response = requests.request("POST", url, data=payload)
  return response

