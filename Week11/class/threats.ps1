# Array of websites containing threat intel
$drop_urls = @('https://rules.emergingthreats.net/blockrules/emerging-botcc.rules',
 'https://rules.emergingthreats.net/blockrules/compromised-ips.txt')

# Loop through the URLS for the rules list
foreach ($u in $drop_urls) {
    # Extract the file name from the URL
    $temp = $u.split("/")
    # load the last element of the array into the variable $file_name
    $file_name = $temp[4]
    
    # Download the files to the current directory if they don't exist already
    if (Test-Path $file_name) {
        continue
    } else {
        Invoke-WebRequest -Uri $u -Outfile $file_name
    } # end if statement
} # end foreach loop

# Array containing the filenames
$inputPaths = @('.\emerging-botcc.rules', '.\compromised-ips.txt')

# Create a regex search to extract IP addresses from emerging-botcc.rules
$regexDrop = '\b((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\b'

# Use that regex search to extract IP addresses from emerging-botcc.rules
Select-String -Path $inputPaths -Pattern $regexDrop |`
 ForEach-Object { $_.Matches } | ForEach-Object { $_.Value } | Sort-Object | Get-Unique |`
 Out-File -FilePath '.\ips-bad.tmp'

# Get the ip addresses discovered, loop through, and insert it into IPTABLES rules
# example: 203.0.113.122 -> `iptables -A INPUT -s 203.0.113.122 -j DROP`
(Get-Content -Path ".\ips-bad.tmp") | `
ForEach-Object { $_ -replace "^","iptables -A INPUT -s " -replace "$"," -j DROP"}| `
Out-File -FilePath ".\iptables.sh"