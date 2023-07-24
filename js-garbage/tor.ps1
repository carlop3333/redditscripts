#optional parameters
param (
    #auto means "tor.ps1 -auto 1" aka run Tor automatically
    [bool] $auto = $false
)

'tar IS REQUIRED'
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
    cd tor
    ./tor
}
function installTor {
    param (
        [String] $url
    )
    Write-Output 'Installing on: ' + $install.ToString()
    $downloader = New-Object System.Net.WebClient
    #PowerShell is better
    try {
        $downloader.DownloadFile($url, $install)
        tar -xk -f $install 
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
}

function getTor {
    if ($OS.OsName -ge 'Microsoft Windows') { installTor($TorWindows) } 
    elseif ($OS.OsName -ge 'macOS') { installTor($TorMac) }
    else { installTor($TorLinux) } 
}

function main {
    Clear-Host
    'Select the option you want to use:'
    if ($TorInstalled -eq $true -and $auto -eq $false) { Write-Output '1> Run' }
    Write-Output '2> Install'
    if ($TorInstalled -eq $true -and $auto -eq $false) { Write-Output '3> Uninstall' }
    Write-Output '4> Exit'
    $opt = Read-Host

    if ($opt -eq 1 -and $TorInstalled -eq $false) { main }
    elseif ($opt -eq 1 -and $TorInstalled -eq $true) { runTor }
    elseif ($opt -eq 2 -and $TorInstalled -eq $false) { getTor }
    elseif ($opt -eq 1 -and $TorInstalled -eq $true) { <# Do something #> }
}

main