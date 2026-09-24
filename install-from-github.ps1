param(
    [Parameter(Mandatory=$true)]
    [string]$Repository,
    [string]$Version = "v0.3.0"
)

# Public-release installer. No GitHub token is needed for a public repository.
$versionNumber = $Version.TrimStart("v")
$url = "https://github.com/$Repository/releases/download/$Version/gabcli-$versionNumber-py3-none-any.whl"
$temp = Join-Path ([System.IO.Path]::GetTempPath()) "gabcli-$versionNumber.whl"

Write-Host "Downloading GabCli $Version from github.com/$Repository ..."
Invoke-WebRequest -Uri $url -OutFile $temp
python -m pip install --user $temp
Remove-Item $temp -Force -ErrorAction SilentlyContinue
Write-Host "GabCli installed. Run: gabcli"
