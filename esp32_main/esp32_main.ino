#include <WiFi.h>

#include <WebServer.h>

#include <esp32cam.h>

#include <MySQL_Connection.h>

#include <MySQL_Cursor.h>

char hostname[] = "192.168.43.85";
char user[] = "jaw"; // MySQL user login username
char password[] = "123456"; // MySQL user login password

// WiFi card example
char ssid[] = "1212312121"; // your SSID
char pass[] = "eiei1234"; // your SSID Password

// Sample query
char INSERT_SQL[] = "INSERT INTO `mysmazcontrol`.`test` (`id`, `name`, `price`) VALUES ('2', 'two', '1000');";

WebServer server(80);

IPAddress server_ip;
WiFiClient client;
MySQL_Connection conn((Client * ) & client);

static auto loRes = esp32cam::Resolution::find(320, 240);
static auto hiRes = esp32cam::Resolution::find(800, 600);



void query() {
  row_values *row = NULL;
  MySQL_Cursor *cur_mem = new MySQL_Cursor(&conn);
  cur_mem -> execute("SELECT _check from `license-plate`.`open_servo`;");
  column_names * cols = cur_mem -> get_columns();
  do {
    row = cur_mem->get_next_row();
    if(row!=NULL){
      Serial.printf(row->values[0]);
    }
  }while (row != NULL);
  delete cur_mem;
  //server.send(200,x);
  Serial.printf("pass");
  return;
}

void handleBmp() {
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");
  }

  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame -> getWidth(), frame -> getHeight(),
    static_cast < int > (frame -> size()));

  if (!frame -> toBmp()) {
    Serial.println("CONVERT FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CONVERT OK %dx%d %db\n", frame -> getWidth(), frame -> getHeight(),
    static_cast < int > (frame -> size()));

  server.setContentLength(frame -> size());
  server.send(200, "image/bmp");
  WiFiClient client = server.client();
  frame -> writeTo(client);
}

void serveJpg() {
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  
  //Serial.printf("CAPTURE OK %dx%d %db\n", frame -> getWidth(), frame -> getHeight(),
  //static_cast < int > (frame -> size()));

  server.setContentLength(frame -> size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame -> writeTo(client);
}

void handleJpgLo() {
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");
  }
  serveJpg();
}

void handleJpgHi() {
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  
  serveJpg();
}

void handleJpg() {
  server.sendHeader("Location", "/cam-hi.jpg");
  server.send(302, "", "");
}

void handleMjpeg() {
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }

  Serial.println("STREAM BEGIN");
  WiFiClient client = server.client();
  auto startTime = millis();
  int res = esp32cam::Camera.streamMjpeg(client);
  if (res <= 0) {
    Serial.printf("STREAM ERROR %d\n", res);
    return;
  }
  auto duration = millis() - startTime;
  Serial.printf("STREAM END %dfrm %0.2ffps\n", res, 1000.0 * res / duration);
}

void setup() {
  Serial.begin(115200); {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }
  // Begin WiFi section
  WiFi.begin(ssid, pass);
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("http://");
  Serial.println(WiFi.localIP());
  Serial.println("  /cam.bmp");
  Serial.println("  /cam-lo.jpg");
  Serial.println("  /cam-hi.jpg");
  Serial.println("  /cam.mjpeg");

  server.on("/cam.bmp", handleBmp);
  server.on("/cam-lo.jpg", handleJpgLo);
  server.on("/cam-hi.jpg", handleJpgHi);
  server.on("/cam.jpg", handleJpg);
  server.on("/cam.mjpeg", handleMjpeg);

  // End WiFi section
  WiFi.hostByName(hostname, server_ip);
  Serial.print("SQL host IP: ");
  Serial.println(server_ip);
  // End DNS lookup
  Serial.println("DB - Connecting...");
  // 3306
  while (conn.connect(server_ip, 3306, user, password) != true) {
    delay(500);
    Serial.print(".");
  }
  // Initiate the query class instance
  server.begin();
  // Execute the query
  //cur_mem->execute(INSERT_SQL);
  // Note: since there are no results, we do not need to read any data
  // Deleting the cursor also frees up memory used
}



void loop() {
  server.handleClient();
}
