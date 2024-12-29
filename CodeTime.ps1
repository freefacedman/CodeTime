# CodeTime.ps1
# To change the output directory, modify the $basePath variable below

$basePath = "$([Environment]::GetFolderPath('Desktop'))\code_time"

$languages = @{
    "C" = @"
#include <stdio.h>

int main() {
    printf(""Hello World\n"");
    return 0;
}
"@
    "Ruby" = @"
puts 'Hello World'
"@
    "HTML" = @"
<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
"@
    "Java" = @"
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println(""Hello World"");
    }
}
"@
    "PHP" = @"
<?php
echo 'Hello World';
?>
"@
    "Python" = @"
print('Hello World')
"@
    "JavaScript" = @"
console.log('Hello World');
"@
    "Go" = @"
package main

import ""fmt""

func main() {
    fmt.Println(""Hello World"")
}
"@
    "CSharp" = @"
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine(""Hello World"");
    }
}
"@
    "Swift" = @"
print(""Hello World"")
"@
    "Kotlin" = @"
fun main() {
    println(""Hello World"")
}
"@
}

# Create the base directory on the Desktop
New-Item -Path $basePath -ItemType Directory -Force | Out-Null

foreach ($lang in $languages.Keys) {
    $folderPath = Join-Path $basePath $lang
    New-Item -Path $folderPath -ItemType Directory -Force | Out-Null
    $fileName = switch ($lang) {
        "C" { "hello.c" }
        "Ruby" { "hello.rb" }
        "HTML" { "index.html" }
        "Java" { "HelloWorld.java" }
        "PHP" { "hello.php" }
        "Python" { "hello.py" }
        "JavaScript" { "hello.js" }
        "Go" { "hello.go" }
        "CSharp" { "HelloWorld.cs" }
        "Swift" { "hello.swift" }
        "Kotlin" { "HelloWorld.kt" }
        default { "hello.txt" }
    }
    $filePath = Join-Path $folderPath $fileName
    $languages[$lang] | Set-Content -Path $filePath -Force
}
