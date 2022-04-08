# clear the screen
Clear-Host

# Log in to a remote SSH server, save the session ID to a variable
#$SSHSession = (New-SSHSession -ComputerName '192.168.122.1' -Credential (Get-Credential eliminmax) | Select-Object -Property SessionId)

#while ($true){
#    # Prompt user for a command
#    $SSHCommand = Read-Host -Prompt "Command to run: $ "
#    # Run command over the SSH session created above
#    (Invoke-SSHCommand -SessionId $SSHSession.SessionId $SSHCommand).Output
#}

Set-SCPItem -ComputerName '192.168.122.1' -Credential (Get-Credential eliminmax) -Path '.\thing.png'-Destination '/home/eliminmax/Desktop/thing.png'

#Get-SCPItem -ComputerName '192.168.122.1' -Credential (Get-Credential eliminmax) -Destination '.\thing.png' -Path '/home/eliminmax/Desktop/thing.png'

# Close the SSH session
#Remove-SSHSession -SessionId $SSHSession.SessionId