[CmdletBinding()]
Param ([string] $dir = "")

[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$vscExtFolder=$ENV:UserProfile+'\.vscode\extensions'

if ((Test-Path $vscExtFolder) -eq $false) {
    New-Item $vscExtFolder -itemtype directory -force
}

Get-ChildItem $dir *.zip -Name | where {
    $folder = $_ -replace ".zip",""
    if ((Test-Path $vscExtFolder\$folder) -eq $true){
        # [System.Windows.Forms.MessageBox]::Show("$folder is already installed!","Visual Studio Code Extensions Plugin") 
    }
    else{
        expand-archive $dir\$_ -DestinationPath $vscExtFolder
        if ((Test-Path $vscExtFolder\$folder) -eq $true){
        }
		else {
            [System.Windows.Forms.MessageBox]::Show("$folder has been installed failed!","Visual Studio Code Extensions Plugin")           
		}
    }
}

