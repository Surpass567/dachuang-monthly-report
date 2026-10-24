param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Source,
    [string]$OutDir,
    [switch]$Offline
)
$ErrorActionPreference = 'Stop'
$Source = (Resolve-Path -LiteralPath $Source).Path
if ([IO.Path]::GetExtension($Source) -ne '.tex') { throw 'Expected a .tex source file.' }
$sourceDir = Split-Path -Parent $Source
if (-not $OutDir) { $OutDir = Join-Path $sourceDir 'build-latex' }
if (-not [IO.Path]::IsPathRooted($OutDir)) { $OutDir = Join-Path $sourceDir $OutDir }
$OutDir = [IO.Path]::GetFullPath($OutDir)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$engine = Join-Path $PSScriptRoot 'tectonic.exe'
if (-not (Test-Path -LiteralPath $engine)) { $engine = Join-Path $env:LOCALAPPDATA 'LaTeXPortable\tectonic.exe' }
if (-not (Test-Path -LiteralPath $engine)) { throw 'Tectonic is not installed in LocalAppData\LaTeXPortable.' }
$engineHome = Split-Path -Parent $engine
$oldCache = $env:TECTONIC_CACHE_DIR
$oldFonts = $env:FONTCONFIG_FILE
$oldNoProxy = $env:NO_PROXY
Push-Location $sourceDir
try {
    $env:TECTONIC_CACHE_DIR = Join-Path $engineHome 'cache'
    $env:FONTCONFIG_FILE = Join-Path $engineHome 'fonts.conf'
    $proxy = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -ErrorAction SilentlyContinue
    if ($proxy.ProxyEnable -and $proxy.ProxyServer -match '^(?:http://)?(?:127\.0\.0\.1|localhost):(\d+)$') {
        $client = [Net.Sockets.TcpClient]::new()
        try {
            $connection = $client.ConnectAsync('127.0.0.1', [int]$Matches[1])
            try { $null = $connection.Wait(500) } catch {}
            if (-not $client.Connected) { $env:NO_PROXY = '*' }
        } finally { $client.Dispose() }
    }
    $engineArgs = @('--synctex', '--keep-logs', '--keep-intermediates', '--outdir', $OutDir)
    if ($Offline) { $engineArgs += '--only-cached' }
    # Explicit search paths are required: Tectonic does not use TeX Live's TEXINPUTS.
    # Shared template takes precedence over stale report-local class copies.
    $cursor = $sourceDir
    $paths = [Collections.Generic.List[string]]::new()
    while ($cursor) {
        foreach ($folder in @('template', 'templates')) {
            $candidate = Join-Path $cursor $folder
            if (Test-Path -LiteralPath $candidate -PathType Container) { $paths.Add($candidate) }
        }
        if (Test-Path -LiteralPath (Join-Path $cursor '.git')) {
            $reports = Join-Path $cursor 'reports'
            if (Test-Path -LiteralPath $reports -PathType Container) { $paths.Add($reports) }
            break
        }
        $parent = Split-Path -Parent $cursor
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
    $paths.Add($sourceDir)
    foreach ($path in ($paths | Select-Object -Unique)) { $engineArgs += @('-Z', ('search-path=' + $path)) }
    $engineArgs += $Source
    & $engine @engineArgs
    if ($LASTEXITCODE -ne 0) { throw "LaTeX compilation failed (exit $LASTEXITCODE). See $OutDir" }
    $pdf = Join-Path $OutDir ([IO.Path]::GetFileNameWithoutExtension($Source) + '.pdf')
    if (-not (Test-Path -LiteralPath $pdf)) { throw "Compiler did not produce $pdf" }
    Write-Host ('PDF: ' + $pdf)
} finally {
    $env:TECTONIC_CACHE_DIR = $oldCache
    $env:FONTCONFIG_FILE = $oldFonts
    $env:NO_PROXY = $oldNoProxy
    Pop-Location
}
