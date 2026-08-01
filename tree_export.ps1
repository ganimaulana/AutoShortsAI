$output = "tree.txt"

Get-ChildItem -Recurse |
Where-Object {
    $_.FullName -notmatch '\\.venv\\' -and
    $_.FullName -notmatch '\\node_modules\\' -and
    $_.FullName -notmatch '\\.git\\' -and
    $_.FullName -notmatch '\\__pycache__\\'
} |
Select-Object FullName |
Out-File $output -Encoding utf8

Write-Host "Done! Output: tree.txt"