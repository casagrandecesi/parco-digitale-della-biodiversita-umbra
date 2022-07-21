param($command)

function Get-Hugo {
    if ($IsWindows) { Join-Path "$PSScriptRoot" "tools/hugo/Windows/x86_64/hugo.exe" }
    elseif ($IsLinux) { Join-Path "$PSScriptRoot" "tools/hugo/Linux/x86_64/hugo" }
    elseif ($IsMacOS) { Join-Path "$PSScriptRoot" "tools/hugo/Darwin/x86_64/hugo" }
    else { 'hugo' }
}

function Get-MultiPathSeparator {
    if ($IsWindows) { ';' }
    else { ':' }
}

if (!(Test-Path "$PSScriptRoot/tools")) { 
    New-Item tools -Type Directory 
}

$hugo = Get-Hugo
Write-Output "Hugo executable: $hugo"
Write-Output ''

if ($command -eq "server") {
    $hugo = Get-Hugo
    Invoke-Expression "$hugo server"
}
elseif ($command -eq "upload") {
    $downloadUrl = 'https://raw.githubusercontent.com/pbswengineering/hugo-uploader/master/hugo-uploader'
    $hugoUploader = Join-Path "$PSScriptRoot" "tools/hugo-uploader"
    $removeUnusedWpContent = Join-Path "$PSScriptRoot" "tools/remove-unused-wp-content.py"
    $optimizedFeaturedImages = Join-Path "$PSScriptRoot" "tools/optimize-featured-images.py"
    Invoke-WebRequest "$downloadUrl" -OutFile "$hugoUploader"
    # Even if the upload didn't work, go ahead, shall you have
    # an already downloaded copy
    if (Test-Path "$hugoUploader") {
        $hugoDir = Split-Path "$hugo" -Parent
        $sep = Get-MultiPathSeparator
        $Env:PATH = "$hugoDir$sep$Env:PATH"
        Invoke-Expression "python $optimizedFeaturedImages"
        Invoke-Expression "$hugo --minify"
        Invoke-Expression "python $removeUnusedWpContent"
        Invoke-Expression "python $hugoUploader"
    } else {
        Write-Output "$hugoUploader doesn't exist and it cannot be downloaded."
        Write-Output ''
    }
}
elseif ($command -eq "public") {
    Invoke-Expression "$hugo --minify"
}
elseif ($command -eq "clean") {
    if (Test-Path public) { Remove-Item -Recurse -Force public }
    if (Test-Path resources) { Remove-Item -Recurse -Force resources }
}
else {
    Write-Output 'Usage: make.ps1 TARGET'
    Write-Output ''
    Write-Output 'Available targets: '
    Write-Output ''
    Write-Output '   server    Start the local development server'
    Write-Output '   upload    Upload the website to the FTP server'
    Write-Output '   public    Compile the website in the public/ directory'
    Write-Output '   clean     Remove hugo-generated files and directories'
    Write-Output ''
}