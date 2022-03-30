# I was originally following along on with the video on array-ctrl, my linux (Pop!_OS 21.10)
# System, until it got to Get-Service, which does not exist on powershell for Linux, so 
# The initial comments are missing from this document.

$OutFilePath = "C:\Users\Eli Array Minkoff\Desktop\services.csv"

# Get a list of system services and their properties, and write it to a CSV file at 
# $OutFilePath
# Get-Service | Select-Object Status, Name, DisplayName, BinaryPathName | Export-Csv -Path `
# $OutFilePath

Get-Service | Where-Object { $_.Status -eq "Running" }

# Check to see if $OutFilePath exists, and print a message if it does
if (Test-Path $OutFilePath) {

    Write-Host -BackgroundColor DarkGreen -ForegroundColor White "Found services.csv."

} else {
    
    Write-Host -BackgroundColor DarkRed -ForegroundColor White "Did not find services.csv."
}