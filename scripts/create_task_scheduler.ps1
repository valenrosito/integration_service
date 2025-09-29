
param(
  [string]$PythonExe = "$(Get-Command python).Source",
  [string]$ProjectRoot = "$PSScriptRoot\..",
  [int]$EveryMin = 10
)

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "-m integration_service.main"
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes $EveryMin) -RepetitionDuration ([TimeSpan]::MaxValue)
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "IntegrationServiceSync" -Action $Action -Trigger $Trigger -Settings $Settings -Description "MSSQL -> API sync every $EveryMin min"
Write-Host "Tarea programada creada (cada $EveryMin min)."
