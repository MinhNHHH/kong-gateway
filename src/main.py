from kong_api import (create_new_service, create_route_service, 
                        proxy_cache, get_detail_routes_services, 
                        remove_service, remove_routes)
import cfg
import argparse

HTTP_STATUS_CONFLICT = 409 # service exist in kong database.
HTTP_STATUS_OK = 200
services = cfg.get_default("services")
plugins_globally =  cfg.get_default("plugins_globally").get("config")

parser = argparse.ArgumentParser(description='Update Microservice')
parser.add_argument('--proxy-cache', action="store_true", help="Config proxy-cache for globally")
parser.add_argument('--remove-service', '--list', action="append",default=[],help="remove service")
args = parser.parse_args()

def main():
  """
    We want to register a new service to the Kong gateway without having to run it manually. 
    So we have a script to update new services as well as keep track of services registered in Kong.
  """
  if len(args.remove_service) > 0:
    # We will remove the specified service
    for service_name in args.remove_service:
      response = get_detail_routes_services(service_name)
      if response.status_code == HTTP_STATUS_OK:
        routes_id = response.json()['data'][-1]['id']
        remove_routes(routes_id, service_name)
        remove_service(service_name)
        print(f"Remove success {service_name}")
  else:
    for service in services:
      new_service = create_new_service(service['name'], service['host'], service['port'])
      if new_service.status_code != HTTP_STATUS_CONFLICT:
        create_route_service(service['name'], service['routes']['paths'])
        print(f"Updated success {service['name']}")
    if args.proxy_cache:
      # We want to cache for all service in Kong
      proxy_cache(plugins_globally['request_method'], plugins_globally['response_code'], 
        plugins_globally['content_type'], plugins_globally['cache_ttl'], plugins_globally['strategy'])

if __name__ == '__main__':
  main()