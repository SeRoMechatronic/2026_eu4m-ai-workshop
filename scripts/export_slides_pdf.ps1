# Exporta las cuatro presentaciones a PDF con PowerPoint (solo Windows con Office).
# Las notas del orador se exportan aparte, como texto, con scripts/export_offline.py.
#
#   powershell -File scripts/export_slides_pdf.ps1 -OutDir dist/instructor_kit/offline
param(
    [Parameter(Mandatory = $true)][string]$OutDir
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$slides = Join-Path $root "slides"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$outFull = (Resolve-Path $OutDir).Path

$ppSaveAsPDF = 32

$app = New-Object -ComObject PowerPoint.Application
try {
    foreach ($deck in Get-ChildItem -Path $slides -Filter "module_*.pptx") {
        $presentation = $app.Presentations.Open($deck.FullName, $true, $false, $false)
        try {
            $pdf = Join-Path $outFull ($deck.BaseName + "_diapositivas.pdf")
            $presentation.SaveAs($pdf, $ppSaveAsPDF)
            Write-Host "PDF  $($deck.BaseName)"
        }
        finally {
            $presentation.Close()
        }
    }
}
finally {
    $app.Quit()
}
