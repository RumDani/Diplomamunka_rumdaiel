# ROS diagnosztikai kimenetek

A mappában található TF-fa és ROS topicgráf fájlok korábbi futások
pillanatképei. Nem bizonyítják a jelenlegi kód futásidejű helyességét; készíts
friss ábrát a `simulation.launch.py` és a `visualization.launch.py` futása alatt.

Ebből a könyvtárból futtasd a `ros2 run tf2_tools view_frames --output frames`
parancsot; az aktuális TF-fa `frames.gv` és `frames.pdf` fájlokba kerül.
A PDF-et az `xdg-open frames.pdf` paranccsal nyithatod meg terminálból.
Az élő transzformáció ellenőrzésére használd a
`ros2 run tf2_ros tf2_echo odom base_scan` parancsot. Az `rqt_graph` a ROS
node-ok és topicok kapcsolatait mutatja, nem a TF-fát.

Az időbélyeges `frames_*.gv/.pdf`, `tf2_frames_latest.gv/.pdf` és
`rosgraph*.png` fájlok korábbi futásokból származó pillanatképek. A teljes
indítási sorrendért és parancsokért lásd a csomag README-jének 4-6. terminálját.