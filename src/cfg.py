"""
Config module of social listening
"""
import yaml
from yaml.parser import ParserError
from dotenv import load_dotenv
from functools import partial
import os, re

ENV_DEFAULT = {
  "CONFIG_PATH": "./kong.yaml"
}
_var_matcher = re.compile(r"\${([^}^{]+)}")
_tag_matcher = re.compile(r"[^$]*\${([^}^{]+)}.*")


def load_env():
  """
  Loading all environments variable that has a SL_ prefix and strip it.
  SL_PG_DB_NAME => PG_DB_NAME
  To get this env, call `get_default("PG_DB_NAME")`
  """
  cfg = ENV_DEFAULT
  load_dotenv()
  # TODO: add supports for nested config using env
  # Probably split by "."
  for env in os.environ:
    if env.startswith("SL_"):
      env_name = env.removeprefix("SL_")
      cfg[env_name] = os.environ[env]
  return cfg

def _path_constructor(_loader, node):
  def replace_fn(match):
      envparts = f"{match.group(1)}:".split(":")
      return os.environ.get(envparts[0], envparts[1])
  return _var_matcher.sub(replace_fn, node.value)

def load_yaml(filename: str) -> dict:
  yaml.add_implicit_resolver("!envvar", _tag_matcher, None, yaml.SafeLoader)
  yaml.add_constructor("!envvar", _path_constructor, yaml.SafeLoader)
  try:
    with open(filename, "r") as f:
      return yaml.safe_load(f.read())
  except (FileNotFoundError, PermissionError, ParserError):
    return dict()


def get(cfg, *path, required=True):
  """
  Get a config with path.
  `path` could be a string for a top-level config or an array for nested config.
  config = {
    "first": {
      "second": "42"
    }
  }
  # get all level config
  >> get(config)
  => {
    "first": {
      "second": "42"
    }
  }
  # get top level config
  >> get(config, "first")
  => {
      "second": "42"
  }
  # get nested config
  >> get(config, "first", "second")
  => 42
  Parameters
  ----------
    path: str
      a path to config
    requried: boolean
      if `True`, raise an exception if the config is not found
  Returns
  -------
    dict | str | None
    The config for given path. In case config not found returns `None`
  """
  def _get(cfg, k, required):
    try:
      cfg = cfg[k]
    except Exception:
      if required:
        raise Exception(f"Failed to get config with path: {path}")
      return None
    return cfg

  value = cfg
  for k in path:
    value = _get(value, k, required)
  return value

def get_int(cfg, *path, required=False):
  """
  Like `get` but try to cast the returned values to integer.
  """
  value = get(cfg, *path, required=required)
  return None if value == None else int(value)

def load_default_config():
  config = {}
  config_env = load_env()
  config.update(config_env)

  # load env after yaml so that we could override config using env
  yaml_path = get(config_env, "CONFIG_PATH")
  config.update(load_yaml(yaml_path))
  return config

########################### Default ###########################
CFG = load_default_config()
# get the default config
get_default = partial(get, CFG)          # get_default("PG_DB_NAME")
get_int_default = partial(get_int, CFG)  # get_int_default("jobs", "interval", "day")