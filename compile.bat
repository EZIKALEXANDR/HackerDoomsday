pyinstaller --onefile --windowed ^
--name "HackerDoomsday" ^
--icon "appicon.ico" ^
--uac-admin ^
--add-data "resources/Hacker.mp4;resources" ^
--add-data "resources/Hacker2.mp4;resources" ^
--add-data "resources/BTDevManager.exe;resources" ^
--add-data "resources/background1.jpg;resources" ^
--add-data "resources/background2.jpg;resources" ^
--add-data "resources/background3.jpg;resources" ^
--add-data "resources/background4.jpg;resources" ^
--add-data "resources/bg.jpg;resources" ^
--add-data "resources/1.jpg;resources" ^
--add-data "resources/2.jpg;resources" ^
--add-data "resources/3.jpg;resources" ^
--add-data "resources/4.jpg;resources" ^
--add-data "resources/5.jpg;resources" ^
--add-data "resources/1.ico;resources" ^
--add-data "resources/2.ico;resources" ^
--add-data "resources/4.ico;resources" ^
--add-data "resources/6.ico;resources" ^
--add-data "resources/runapp_main.MP3;resources" ^
--add-data "resources/after50.mp3;resources" ^
--add-data "resources/scaryfor3.MP3;resources" ^
--version-file version_info.txt ^
main.py

pause
