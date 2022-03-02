"""Tools for managing an SSH connection"""
import paramiko
from getpass import getpass


def new_password_connection(user, host, port=22):
    """Initialize and authenticate a connection"""
    # Set up the connection name for use in interactive prompts
    connection_name = f"{user}@{host}"
    if port != 22:
        connection_name += ":22"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Get the password and initialize the connection
    for _ in range(3):
        password = getpass(prompt=f"Password for {connection_name}: ")
        # Try to connect with the provided password and return the client
        try:
            client.connect(host, port, user, password)
            return client
        # In case of authentication error, print exception, then loop again
        except paramiko.AuthenticationError:
            print(f'Authentication Failed for {connection_name}.')
    # This can only run if the return statement above never did
    else:
        # Raise an exception authentication fails 3 times
        raise ValueError(f"Failed to authenticate {connection_name}")
