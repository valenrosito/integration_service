
$taskName = "IntegrationServiceSync"
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
  Write-Host "Tarea programada eliminada."
} else {
  Write-Host "No existía la tarea programada."
}
