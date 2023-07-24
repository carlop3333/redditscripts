#optional parameters
param (
    #auto means "tor.ps1 -auto 1" aka run Tor automatically
    [bool] $auto = $false,
    [bool] $autotemp = $false
)



'tar IS REQUIRED'
# Just in case
$autotempWarn = $False
# Basic shit
$OS = Get-ComputerInfo -Property OsName
$TorInstalled = Test-Path 'tor-file.tar.gz'
$install = Join-Path $Pwd.Path 'tor-file.tar.gz'
#Links for you-know-what
$TorWindows = "https://archive.torproject.org/tor-package-archive/torbrowser/12.5.1/tor-expert-bundle-12.5.1-windows-x86_64.tar.gz"
$TorLinux = "https://archive.torproject.org/tor-package-archive/torbrowser/12.5.1/tor-expert-bundle-12.5.1-linux-x86_64.tar.gz"
$TorMac = "https://archive.torproject.org/tor-package-archive/torbrowser/12.5.1/tor-expert-bundle-12.5.1-macos-x86_64.tar.gz"

function runTor {
    'Running Tor...'
    Start-Sleep -Seconds 2
    ./tor/tor
}
function installTor {
    param (
        [String] $url
    )
    Write-Output "Installing on: $install" 
    #PowerShell is better
    try {
        Invoke-WebRequest -Uri $url -OutFile $install
        tar -xk -f $install 'tor'
        Write-Output 'Tor installed!'
        runTor 
    }
    catch [System.Net.WebException] {
        Write-Error "Oopsie... Seems we're unable to download the file..."
    }
    catch [System.IO.IOException] {
        Write-Error "Oh shit we don't have perms to read/write..."
    }
    catch {
        Write-Error "An Unknown Error happened...."
    }
    
    
}

function uninstallTor {
    Remove-Item $install
    Remove-Item -Recurse (Join-Path $Pwd.Path 'tor') 
    "Tor uninstalled!"
    exit
}

function getTor {
    if ($OS.OsName -ge 'Microsoft Windows') { installTor($TorWindows) } 
    elseif ($OS.OsName -ge 'macOS') { installTor($TorMac) }
    else { installTor($TorLinux) } 
}

function main {
    Clear-Host
    'Run this on the folder you want Tor to Install!'
    'Select the option you want to use:'
    if ($TorInstalled -eq $true) { Write-Output '1> Run' }
    if ($TorInstalled -eq $false) { Write-Output '2> Install' }
    if ($TorInstalled -eq $true) { Write-Output '3> Uninstall' }
    Write-Output '4> Exit'
    $opt = Read-Host

    #ugh
    if ($opt -eq 1 -and $TorInstalled -eq $false) {main}
    elseif ($opt -eq 1 -and $TorInstalled -eq $true) {runTor}
    elseif ($opt -eq 2 -and $TorInstalled -eq $false) {getTor}
    elseif ($opt -eq 2 -and $TorInstalled -eq $true) {main}
    elseif ($opt -eq 3 -and $TorInstalled -eq $false) {main}
    elseif ($opt -eq 3 -and $TorInstalled -eq $true) {uninstallTor}
}

if ($autotemp -eq $true) {
    # Check that is not already installed
    if ($TorInstalled -eq $false) {
        getTor
        runTor
    } else {
        Write-Warning 'Detected tor installation, it will be treated as -auto param'
        $autotempWarn = $true
        runTor
    }
}

if ($auto -eq $true) {
    if ($TorInstalled -eq $true) {
        runTor
    }
    else {
        "You almost did the today's TIFU... install Tor FIRST!"
        Exit
    }
}

main

