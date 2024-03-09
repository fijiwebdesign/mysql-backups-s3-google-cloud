# mysql_utils.py
import subprocess
from urllib.parse import urlparse, parse_qs

# Specify the full path to mysqldump
mysqldump_path = '/usr/bin/mysqldump'

def mysqldump_from_url(url, output_file):
    # Parse the connection URL string
    parsed_url = urlparse(url)

    # Extract connection parameters
    db_params = parse_qs(parsed_url.query)
    host = parsed_url.hostname
    port = parsed_url.port
    username = parsed_url.username
    password = parsed_url.password
    database = parsed_url.path.lstrip('/')

    # Build mysqldump command
    mysqldump_cmd = [
        mysqldump_path,
        '-h', host,
        '-P', str(port),
        '-u', username,
        '-p' + password,
        database
    ]

    # Execute mysqldump command and write output to file
    with open(output_file, 'w') as f:
        subprocess.call(mysqldump_cmd, stdout=f)
