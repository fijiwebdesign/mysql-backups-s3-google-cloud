import os
import yaml
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

# Convert the dictionary to a list of dictionaries
env_vars_list = [{'name': key, 'value': value} for key, value in env_vars.items()]


# Convert environment variables to YAML format
yaml_data = yaml.dump({
  "env": env_vars_list
}, default_flow_style=False)

# Print the YAML data
print(yaml_data)