# ════════════════════════════════════════════════════════════════════
# FakeMètre — duplication des images en versions _fr / _en
# ════════════════════════════════════════════════════════════════════
#
# UTILISATION :
#   1. Dépose tes images dans le dossier "images/" en les nommant SANS
#      suffixe de langue, ex :  russie_pluton.jpg   wombat_crottes.png …
#      (le nom de base doit figurer dans la liste $BASES ci-dessous)
#   2. Lance ce script :   .\dupliquer_images.ps1
#   3. Il crée pour chacune  <nom>_fr.jpg  ET  <nom>_en.jpg
#      (toujours en .jpg, car c'est ce que le jeu attend)
#
# Idempotent : relançable sans risque. Par défaut il N'ÉCRASE PAS une
# version _fr/_en déjà présente ; ajoute  -Force  pour forcer.
# ════════════════════════════════════════════════════════════════════

param([switch]$Force)

$ErrorActionPreference = 'Stop'
$imagesDir = Join-Path $PSScriptRoot 'images'

# Les 13 visuels attendus par les nouvelles questions
$BASES = @(
  'post_vie_labo','post_climat_2027','humains_singes','russie_pluton',
  'cleopatre_iphone','lac_vostok','aura_corps','tyrolienne','diomede',
  'univers_etoiles','wombat_crottes','chevre_pupille','meduse_immortelle'
)

if (-not (Test-Path $imagesDir)) {
  Write-Host "Dossier introuvable : $imagesDir" -ForegroundColor Red
  exit 1
}

$created = 0; $skipped = 0; $missing = @()

foreach ($base in $BASES) {
  # cherche un fichier source <base>.<ext> (hors versions _fr/_en déjà suffixées)
  $src = Get-ChildItem -Path $imagesDir -File |
         Where-Object { $_.BaseName -eq $base } |
         Select-Object -First 1

  if (-not $src) {
    # déjà dupliqué ? alors ce n'est pas "manquant"
    $hasFr = Test-Path (Join-Path $imagesDir "${base}_fr.jpg")
    $hasEn = Test-Path (Join-Path $imagesDir "${base}_en.jpg")
    if (-not ($hasFr -and $hasEn)) { $missing += $base }
    continue
  }

  foreach ($lang in @('fr','en')) {
    $dest = Join-Path $imagesDir "${base}_${lang}.jpg"
    if ((Test-Path $dest) -and -not $Force) {
      Write-Host "  = existe deja : ${base}_${lang}.jpg (utilise -Force pour ecraser)" -ForegroundColor DarkGray
      $skipped++
    } else {
      Copy-Item -Path $src.FullName -Destination $dest -Force
      Write-Host "  + cree : ${base}_${lang}.jpg  (depuis $($src.Name))" -ForegroundColor Green
      $created++
    }
  }
}

Write-Host ""
Write-Host "Termine : $created creees, $skipped ignorees." -ForegroundColor Cyan
if ($missing.Count) {
  Write-Host "Pas encore de source pour : $($missing -join ', ')" -ForegroundColor Yellow
}
