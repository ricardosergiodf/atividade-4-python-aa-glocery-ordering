$exclude = @("venv", "ativ-pratica-4-python-aa.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "ativ-pratica-4-python-aa.zip" -Force