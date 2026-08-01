$root = Get-Location
$output = Join-Path $root "project_dump.txt"

if (Test-Path $output) {
    Remove-Item $output
}

Add-Content $output "============================="
Add-Content $output "PROJECT STRUCTURE"
Add-Content $output "============================="

tree /A /F | Out-File -Append $output

$excludeFolders = @(
".git",
".venv",
"node_modules",
"__pycache__",
"dist",
"build",
"output",
"projects",
"logs",
"temp",
".pytest_cache"
)

$extensions = @(
".py",
".js",
".ts",
".tsx",
".json",
".toml",
".yaml",
".yml",
".md"
)

Get-ChildItem -Recurse -File | Where-Object {

    $allowed = $extensions -contains $_.Extension

    $blocked = $false

    foreach($f in $excludeFolders){
        if($_.FullName -match "\\$f\\"){
            $blocked = $true
            break
        }
    }

    $allowed -and -not $blocked

} | ForEach-Object {

    Add-Content $output ""
    Add-Content $output "=================================================="
    Add-Content $output "FILE : $($_.FullName)"
    Add-Content $output "=================================================="
    Get-Content $_.FullName | Add-Content $output
}

Write-Host ""
Write-Host "DONE!"
Write-Host "Output:"
Write-Host $output