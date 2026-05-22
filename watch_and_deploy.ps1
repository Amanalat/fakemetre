# ─────────────────────────────────────────
#  Auto-deploy FakeMetre
#  Lance ce script une fois, laisse-le tourner.
#  Il deploie automatiquement des que index.html est modifie.
# ─────────────────────────────────────────

$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$file   = "index.html"

Write-Host "Surveillance de $folder\$file" -ForegroundColor Cyan
Write-Host "Ctrl+C pour arreter.`n" -ForegroundColor DarkGray

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path   = $folder
$watcher.Filter = $file
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite
$watcher.EnableRaisingEvents = $true

# Delai anti-doublon (certains editeurs sauvegardent 2 fois de suite)
$lastDeploy = [datetime]::MinValue

$action = {
    $now = Get-Date
    if (($now - $script:lastDeploy).TotalSeconds -lt 5) { return }
    $script:lastDeploy = $now

    Write-Host "`n[$now] Modification detectee - deploiement en cours..." -ForegroundColor Yellow

    Set-Location $folder

    git add index.html
    git commit -m "Mise a jour automatique $now"
    git push

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Deploy OK !" -ForegroundColor Green
    } else {
        Write-Host "Erreur lors du push. Verifie ta connexion ou ton depot." -ForegroundColor Red
    }
}

Register-ObjectEvent $watcher Changed -Action $action | Out-Null

# Boucle infinie : le script reste actif
try {
    while ($true) { Start-Sleep -Seconds 1 }
} finally {
    $watcher.Dispose()
}
