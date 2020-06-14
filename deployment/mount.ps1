Mount-DiskImage "$HOME\mullebil.iso"
$letter = (Get-DiskImage "$HOME\mullebil.iso"| get-volume).DriveLetter + ':'
cmd /c mklink /d $HOME\mullebil $letter