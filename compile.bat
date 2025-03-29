pyinstaller --onefile --windowed --noconsole ^
--name "HackerDoomsday" ^
--icon "appicon.ico" ^
--uac-admin ^
--optimize=2 ^
--clean ^
--add-data "Hacker.mp4;resources" ^
--add-data "Hacker2.mp4;resources" ^
--add-data "background1.jpg;resources" ^
--add-data "background2.jpg;resources" ^
--add-data "background3.jpg;resources" ^
--add-data "background4.jpg;resources" ^
--add-data "bg.jpg;resources" ^
--add-data "1.jpg;resources" ^
--add-data "2.jpg;resources" ^
--add-data "3.jpg;resources" ^
--add-data "4.jpg;resources" ^
--add-data "5.jpg;resources" ^
--add-data "1.ico;resources" ^
--add-data "2.ico;resources" ^
--add-data "4.ico;resources" ^
--add-data "6.ico;resources" ^
--add-data "runapp_main.MP3;resources" ^
--add-data "after50.mp3;resources" ^
--add-data "scaryfor3.MP3;resources" ^
--add-data "script.vbs;resources" ^
--add-data "start.bat;resources" ^
--version-file version_info.txt ^
main.py

pause