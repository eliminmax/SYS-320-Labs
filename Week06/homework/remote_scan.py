#!/usr/bin/python3
from pathlib import Path
import yaml
import sys

import misc_util
import remote_tools


def load_commands(command_file):
    """Load commands to run on the remote server from a YAML file
    """
    with open(command_file) as f:
        raw_yaml_data = yaml.safe_load(f)
    return raw_yaml_data


def ask_delete_file(path):
    """Given a pathlib.Path object, ask the user whether to delete it or not.
    """
    # Safer to assume that we should keep the file than delete it.
    should_delete = misc_util.prompt_yn(
        f"There is already a file at {path}. Delete it?", default='n')
    if should_delete:
        # pathlib.Path.unlink() removes a regular file or symlink
        path.unlink()
        return path
    else:
        # If the file is still here, we can't save the output - exit gracefully
        sys.exit()


def send_fs_file(ssh_client):
    """Send fs.py over sftp, move it to /usr/bin, chown it to root, chmod +x.
    Must have passwordless sudo on the server
    """
    # Copy fs.py to the server
    sftp = ssh_client.open_sftp()
    sftp.put('fs.py', 'fs.py')
    sftp.close()
    # Make it executable
    ssh_client.exec_command('chmod 755 fs.py')


def main():
    # Define variables
    user = 'eliminmax'  # The username I default to
    host = 'sys320w06'  # SYS-320 week 06 - a fresh Ubuntu Server libvirt VM
    port = 22
    # Outfile will be named eli@sys320w06h:22.ssh-datacapture
    outfile_name = f'{user}@{host}:{port}.ssh-datacapture'
    outfile = Path.cwd().joinpath(outfile_name)
    # If the file exists, ask to delete it. If user says no, exit
    if outfile.is_file():
        ask_delete_file(outfile)
    # Initialize the SSH client
    # This function prompts the user for a password and returns an SSHClient
    ssh_client = remote_tools.new_password_connection(user, host, port)
    # send fs.py to the server
    send_fs_file(ssh_client)
    # execute `sudo fs.py -d /usr/bin` on the server, saving stdout to outfile
    stdin, stdout, stderr = ssh_client.exec_command(
        'sudo ./fs.py --directory /usr/bin')
    with open(outfile, 'w') as f:
        outfile.write(stdout)


if __name__ == '__main__':
    main()
