Bitte erstelle ein Python script, welches ein Memory Spiel grafisch darstellt.

Es soll dabei aus insgesamt 16 Karten bestehen, also 8 Paaren, angeordnet in 4x4.
Es spielen 2 Spieler gegeneinander, indem sie auf die Karten klicken können.
Es gelten allgemein die normalen Regeln von dem Spiel Memory.

Die Kartenbilder sollen personalisiert sein, also ich möchte 8 Bilder im Code angeben können, welche verwendet werden sollen.

Zudem soll der aktuelle Spielstand angezeigt werden - also Spieler 1 und Spieler 2, für beide sollen Namen eingegeben werden können
zu beginn einen spiels. Die Karten sollen toll aufgedeckt werden können durch eine Drehung.


Pre-requisites:

pip install pillow

memory_game.py
images/
 ├─ img1.png
 ├─ img2.png
 ├─ img3.png
 ├─ img4.png
 ├─ img5.png
 ├─ img6.png
 ├─ img7.png
 ├─ img8.png
 └─ back.png   # Rückseite der Karten

-----------------------------------------

pre-requisite for advanced setup:

pip install pillow pygame


Hinweise

Bilderauswahl:

Startmenü → „Bilder auswählen“ → genau 8 Bilder

Rückseite: images/back.png

Soundeffekte:

Flip: sounds/flip.wav

Treffer: sounds/match.wav

Fehler: sounds/fail.wav

Modernes Layout:

Hintergrund dunkel (#2E3440), Karten abgerundet

Punkteanzeige oben

Menü „Neustart / Beenden“