# List contents in the .\Documents directory
# List all files and print the full path
# Get-ChildItem -Recurse -Include *.docx,*.txt,*.pdf -Path .\Documents |`
# Select FullName
# Get-ChildItem -Recurse -Include *.docx,*.txt,*.pdf -Path .\Documents |`
# Export-Csv -Path files.csv

# Import CSV File
$fileList = Import-Csv -Path files.csv # -header FullName

# Loop through the results
foreach ($f in $fileList) {
    Get-ChildItem -Path $f.FullName
}
