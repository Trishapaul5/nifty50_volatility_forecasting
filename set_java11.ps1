$env:JAVA_HOME = "C:\Program Files\Java\jdk-11"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
Write-Output "JAVA_HOME set to $env:JAVA_HOME"
java -version
