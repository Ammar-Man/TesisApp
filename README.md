# ArcadaRobot
pip freeze > requirements.txt

python -m venv .venv

deactivate

pip freeze > requirements.txt
1.  python -m venv .venv-rpi
2.  .venv\Scripts\activate
3.  pip install -r requirements.txt
4. run pythons.script

## To start robot app you need to run 
0. Adjust folder names to match your local folders.
   - 0.1 In "Linux/Flask/chatboot/RunListenToice.py," modify sys.path.append('D:/yourfolder../ArcadaRobot/Linux/Flask/chatboot').
   - 0.2 In "Linux/Flask/Start_Tablet_html.py," update directory = ("D:/yourfolder.../ArcadaRobot/Linux/Tablet").

Run Linux.bat will 
-  Execute Camera_expression.py.
-  Execute LinuxServer.py.
-  Execute Start_Tablet_html.py.
Run PRI.bat will
-  Execute RPiServer.py.

1. The Camera expression functionality is implemented in the file Camera_expression.py and operates on port 1500.
   - This code provides three options:
     - 1.1 @app.route('localhost:1500/expression_start') to capture facial expressions from the camera.
     - 1.2 @app.route("localhost:1500/camera") to access the camera feed.
     - 1.3 @app.route("localhost:1500/stop") to stop the camera and expression capture.

   - The Python code includes two functions:
     - The function def generate_expression() captures your facial expression using deepface.
     - The function def generate_frames() opens the camera and returns its feed through the endpoint /camera.


2. The LinuxServer functionality serves as the central control unit for various functions within the Robot Snow application. It acts as the main brain, housing a control panel that allows users to open features such as the camera, expressions, sending and fetching API data. This server operates seamlessly on iPhones or any connected device within the same Wi-Fi network.

- Additionally, the LinuxServer includes a chatbot application where users can engage in conversations with the robot, exchanging voice or text messages with it.

3. The Start_Tablet_html.py is a Python script designed to execute the tablet touch screen interface powered by HTML and running on port 5500. It encompasses various components, including 'bootstrap,' CSS, HTML, and JavaScript, all located within the 'Linux/Tablet' folder.

4. The RPiServer.py functions as the primary server for the robot's facial expressions. It receives API requests on the port specified by @app.route('localhost:5000/api/post/face"expressions"'). Upon fetching this API along with expressions, the server responds by sending this information to the FaceLibrary and returns it as an SVG depicting the robot's face. Subsequently, it transmits the expressions to @app.route("/api/stream"), which is responsible for displaying the robot's face on the projector screen with the fetched expressions.





![](images/digram.png)
## Beskrivning
ArcadaRobot är en Linux-baserad applikation utformad för att köra på en tablet med pekskärmssystem. Applikationen har följande funktioner:


----------------------------------------------------------------------------------------------------------------
## Control panel
- **Control panel > index.html:** 
- Denna HTML-sida som innehåller ett formulär där användaren kan ange ett ansiktsuttryck. När användaren skickar formuläret, skickas detta ansiktsuttryck till en specifik API-endpoint (http://localhost:5000/api/post) via en HTTP-förfrågan. Svaret från API:et används för att avgöra om förfrågan var framgångsrik och lagras i lokal lagring (localStorage). Därefter finns det en ström (stream) som uppdaterar robotens ansiktsuttryck.
----------------------------------------------------------------------------------------------------------------
## Face Libaray
- **APi>FaceLibrary > Face_Libray.js:** 
- **command: (`	getFaceByJS ("smile");):**
- Denna kod definierar en lista (face_data) med olika ansiktsuttryck representerade som SVG-path-strängar för munnen, ögonen, och så vidare. Varje ansiktsuttryck har ett unikt id och namn. Det finns även en funktion (createFaceByName) som tar emot ett ansiktsnamn och returnerar den matchande ansiktsdatan från listan i JSON-format.
--------------------------------------------------------------------------------------------------------
### RPi-Face Projector:
- Required Environment:
%pip install flask flask-cors, from queue import Queue ,from flask import Flask, Response, render template, request, from flask cors import CORS

- **APi>Server.ipynb:** 
   - 1- Flask-appen skapas och konfigureras med CORS-aktivering för att tillåta förfrågningar från andra domäner.

   - 2- En kö (queue) skapas för att lagra meddelanden som ska skickas till klienten i realtid.

   - 3 - En rotadress ("/") skapas, där en HTML-sida ("index.html") renderas när användare besöker rotadressen.

    - 4 - En API-rutt ("/api/post") tillåter klienten att skicka data via GET-förfrågningar. Den mottagna datan placeras i kön för realtidskommunikation.

    - 5 -En realtidsdataström skapas med Server-Sent Events (SSE) genom en SSE-rutt ("/api/stream"). Denna rutt tillåter klienten att etablera en SSE-förbindelse för att lyssna på realtidsmeddelanden.

    - 6 -En funktion (event_stream) skickar meddelanden från kön till klienten i en oändlig loop med användning av "yield" för att hantera realtidsuppdateringar.

-  Slutligen startas Flask-webbservern med trådhantering för att hantera flera anslutningar samtidigt.

- I korthet möjliggör denna kod realtidskommunikation mellan servern och klienten genom att använda SSE och en kö för att hantera meddelanden om ansiktsuttryck.
--------------------------------------------------------------------------------------------------------
<!-- API.ipynb -->
### Tablet :
- **Linux > Tablet:** 

- Front-end för surfplattor som kör robotappen med hjälp av CSS, Bootstrap och JavaScript:
  -  Funktionen button():
        Visar en enkel varningsruta med texten "booton" när den kallas.

  -  Funktionen selectedPerson(name):
        Byter innehållet i en HTML-container baserat på det mottagna namnet.
        Använder fetch för att hämta HTML-innehållet från olika filer beroende på det angivna namnet.
        Uppdaterar HTML-innehållet i en given DOM-container.

  -  Funktionen contact():
        Hämtar och visar innehållet från en "people.html"-fil i en specifik DOM-container.

   - Funktionen arcada():
        Hämtar och visar innehållet från en "arcada.html"-fil i en specifik DOM-container.

  -  Funktionen info():
        Hämtar och visar innehållet från en "info.html"-fil i en specifik DOM-container.

  -  Funktionen SendFaceName(int):
        Skickar en ansiktsparameter till en API-slutpunkt (/api/post) baserat på det givna indexet.
        Använder fetch för att göra en asynkron förfrågan till servern.

   - Diverse händelselyssnare:
        Lyssnar på klickhändelser på olika DOM-element och utför olika åtgärder, inklusive navigering till olika sidor och spela upp ljudfiler.

  -  Funktionen delay(ms):
        Returnerar ett Promise som löses efter den angivna fördröjningen i millisekunder.

  -  Funktionen myFunction(int):
        Använder delay för att skapa en fördröjning och loggar meddelanden före och efter fördröjningen.

   - Diverse händelselyssnare för klickbara bilder:
        Lyssnar på klickhändelser på olika bilder och utför olika åtgärder, inklusive att skicka ansiktsparametrar och spela upp ljudfiler med fördröjning.

