# Create command line parameters to copy a file and place into an evidence directory
param(

  [parameter(Mandatory = $true)]
  [int]$ReportNo,

  [parameter(Mandatory = $true)]
  [String]$FilePath

)

# Create a directory with the report number
$reportDir = "rpt$ReportNo"

# Create the directory
mkdir $reportDir

# Copy the file into the new directory
Copy-Item $FilePath $reportDir
