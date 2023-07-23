Write-Output "RUN THIS ON THE FOLDER YOU WANT TO INSTALL TOR!!"
$OS = Get-ComputerInfo -Property OsName
$TorWindows = "https://archive.torproject.org/tor-package-archive/torbrowser/12.5.1/tor-expert-bundle-12.5.1-windows-x86_64.tar.gz"
$TorLinux = "https://archive.torproject.org/tor-package-archive/torbrowser/12.5.1/tor-expert-bundle-12.5.1-linux-x86_64.tar.gz"
$TorMac = "https://archive.torproject.org/tor-package-archive/torbrowser/12.5.1/tor-expert-bundle-12.5.1-macos-x86_64.tar.gz"

function runTor {
    Write-Output "Found tor extract installed, skipping instalation!"
    Write-Output "If you really want to reinstall Tor, delete the tor.tar.gz file!"
}
function installTor {
    param (
        [String] $url
    )
    $install = Join-Path $Pwd.Path 'tor-file.tar.gz'
    Write-Output 'Installing on: ', $install
    Invoke-WebRequest -Uri $url -OutFile $install
}

function getTor {
    param (
        [String] $os
    )
    $tor = Test-Path 'tor-file.tar.gz'
    if ($os -eq "windows" && $tor -eq $false) {
        installTor($TorWindows)
    } elseif ($os -eq "mac" && $tor -eq $false) {
        installTor($TorMac)
    } elseif ($os -eq "linux" && $tor -eq $false) {
        installTor($TorLinux)
    } elseif ( $tor -eq $true) {
        runTor
    }
}

if ($OS.OsName -ge "Microsoft Windows 10") {
    getTor("windows")
} elseif ($OS.OsName -ge "macOS") {
    getTor("mac")
} else {
    getTor("linux")
}