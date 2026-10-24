$ErrorActionPreference = 'Stop'
$utf8 = [Text.UTF8Encoding]::new($false)
$target = Join-Path $env:LOCALAPPDATA 'LaTeXPortable'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = Join-Path $target ('backups\' + $stamp)
New-Item -ItemType Directory -Force -Path $backup | Out-Null
Copy-Item -LiteralPath (Join-Path $target 'compile.ps1') -Destination (Join-Path $backup 'compile.ps1')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'compile.ps1') -Destination (Join-Path $target 'compile.ps1') -Force
$users = @((Join-Path $env:APPDATA 'Code\User'))
foreach ($root in @((Join-Path $env:APPDATA 'Code\User\profiles'), (Join-Path $env:APPDATA 'Code - Insiders\User\profiles'))) {
    if (Test-Path -LiteralPath $root) { $users += @(Get-ChildItem -LiteralPath $root -Directory | Select-Object -ExpandProperty FullName) }
}
if (Test-Path -LiteralPath (Join-Path $env:APPDATA 'Code - Insiders\User')) { $users += (Join-Path $env:APPDATA 'Code - Insiders\User') }
$index = 0
foreach ($userDir in $users) {
    $settingsFile = Join-Path $userDir 'settings.json'
    $settings = [pscustomobject]@{}
    if (Test-Path -LiteralPath $settingsFile) {
        $settings = Get-Content -LiteralPath $settingsFile -Raw -Encoding UTF8 | ConvertFrom-Json
        Copy-Item -LiteralPath $settingsFile -Destination (Join-Path $backup ("settings-$index.json"))
    }
    $values = @{
        'latex-workshop.latex.tools' = @(@{name='global-tectonic'; command=(Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'); args=@('-NoProfile','-ExecutionPolicy','Bypass','-File',(Join-Path $target 'compile.ps1'),'-Source','%DOC_EXT%','-OutDir','%OUTDIR%')})
        'latex-workshop.latex.recipes' = @(@{name='Global Tectonic';tools=@('global-tectonic')})
        'latex-workshop.latex.recipe.default' = 'first'
        'latex-workshop.latex.build.enableMagicComments' = $false
        'latex-workshop.latex.autoBuild.run' = 'onSave'
        'latex-workshop.latex.outDir' = '%DIR%/build-latex'
        'latex-workshop.view.pdf.viewer' = 'tab'
    }
    foreach ($key in $values.Keys) { $settings | Add-Member -NotePropertyName $key -NotePropertyValue $values[$key] -Force }
    # Keep these user settings shared when new VS Code profiles are created.
    $shared = @($settings.'workbench.settings.applyToAllProfiles') + @($values.Keys)
    $settings | Add-Member -NotePropertyName 'workbench.settings.applyToAllProfiles' -NotePropertyValue @($shared | Where-Object { $_ } | Select-Object -Unique) -Force
    [IO.File]::WriteAllText($settingsFile, ($settings | ConvertTo-Json -Depth 30), $utf8)
    Write-Host "Configured: $settingsFile"
    $index++
}
Write-Host "Backup: $backup"
