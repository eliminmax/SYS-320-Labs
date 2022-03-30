$OutFilePath = "C:\Users\Eli Array Minkoff\Desktop\services.csv"

# Get a list of system services and their properties, and write it to a CSV file at 
# $OutFilePath
Get-Service | Select-Object Status, Name, DisplayName, BinaryPathName | Export-Csv -Path `
$OutFilePath

# Check to see if $OutFilePath exists, and print a message if it dows
if (Test-Path $OutFilePath) {

    Write-Host -BackgroundColor DarkGreen -ForegroundColor White`
    "Successfully created `services.csv`."

} else {
    
    Write-Host -BackgroundColor DarkRed -ForegroundColor White`
    "Failed to create `servicess.csv`."
}