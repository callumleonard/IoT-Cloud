function RunFile() {
WshShell = new ActiveXObject("WScript.Shell");
WshShell.Run("scan.bat", 1, false);
}
