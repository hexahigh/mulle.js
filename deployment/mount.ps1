if (-not (Test-Path "$HOME\mullebil.iso" -PathType leaf) ) {
Throw "ISO file not found at $HOME\mullebil.iso"
}

Test-Path "$HOME\mullebil.iso"
Mount-DiskImage "$HOME\mullebil.iso"
$letter = (Get-DiskImage "$HOME\mullebil.iso"| get-volume).DriveLetter + ':'
cmd /c mklink /d $HOME\mullebil $letter