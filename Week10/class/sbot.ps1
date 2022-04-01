# (pretend to) send spam email using Powershell

$toSend = @(
    'eli.minkoff+sbot.ps1.target0@mymail.champlain.edu',
    'eli.minkoff+sbot.ps1.target1@mymail.champlain.edu',
    'eli.minkoff+sbot.ps1.target2@mymail.champlain.edu'
)

# Message Body
$msg = "Hello"


# Send an email every second

while ($true) {
    # loop over target addresses
    foreach ($email in $toSend) {
        # Send the email
        Write-Host "Send-MailMessage -From 'eli.minkoff@mymail.champlain.edu' -To $email -Subject 'Tisk tisk'`
        -Body $msg -SmtpServer X.X.X.X"
        # Pause for 1 second
        start-sleep 1
    }
}