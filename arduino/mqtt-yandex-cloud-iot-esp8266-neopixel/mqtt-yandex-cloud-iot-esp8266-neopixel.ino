#include "cfg.h"
#include "utils.h"
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// WiFi client settings
const char *ssid = _ssid;
const char *password = _password;
bool connectdone = false;

// Yandex CLOUD
const char *mqttServer = "mqtt.cloud.yandex.net";
int mqttPort = 8883;
const char *username = _username;                   // Yandex IoT broker ID 
const char *devicepassword = _devicepassword;       // Yandex IoT broker password 
// Setup IoT
const String deviceId = "device-iot-node-mcu-01";   // unique device id for cloud function
const String commands = String("/yandex-iot-core/" + deviceId + "/commands");

const char *test_sr ="-----BEGIN CERTIFICATE-----\n \
MIIDUzCCAjqgAwIBAgIBADANBgkqhkiG9w0BAQ0FADBDMQswCQYDVQQGEwJ1czEM\n\
MAoGA1UECAwDUFBUMRIwEAYDVQQKDAlsb2NhbGhvc3QxEjAQBgNVBAMMCWxvY2Fs\n\
aG9zdDAeFw0yMTA2MjkxNTQxNDBaFw0yMjA2MjkxNTQxNDBaMEMxCzAJBgNVBAYT\n\
AnVzMQwwCgYDVQQIDANQUFQxEjAQBgNVBAoMCWxvY2FsaG9zdDESMBAGA1UEAwwJ\n\
bG9jYWxob3N0MIIBIzANBgkqhkiG9w0BAQEFAAOCARAAMIIBCwKCAQIAyOJ/chse\n\
W+oAMAKd0s8Z2Rt+c8oh4J2RjX8TapZap0e0hqtlC6Sp5unkTMfQll44oUx33W/d\n\
+9UGdCpXaOqPGD5gVs8nV04dFt1fgsoc1uzVEOOC+0MtwQ4RDtbKdUvD/M6xXilR\n\
wuzcJDH5HKYh/Tx+L7hjK7Mp/Xt6UXQpqtm+hvBdOI4OD7XCOole0maJfiEIk9ik\n\
hACQ2JdkVhsY/sVvkAfiAjsHW6tg1m2mHaOn6j/8KTfFBZOQNcEmErz2/bcIwij/\n\
hm4crKIM85D1dZIigcNJ5C/1wsN3tlwJJacoiAmLMQRFTDkXQnuektdT1YaV7Us1\n\
WTTYas/3PgrnyBcCAwEAAaNQME4wHQYDVR0OBBYEFFYBi5K11aIaXhX7k+DYBTOW\n\
mEMjMB8GA1UdIwQYMBaAFFYBi5K11aIaXhX7k+DYBTOWmEMjMAwGA1UdEwQFMAMB\n\
Af8wDQYJKoZIhvcNAQENBQADggECAAKg2cHHfIYRtPvVkLtcS5ducbzQtW4O15C7\n\
i7YuMo4YllfWy9J57/QXf9JeaA13S1/ptc6lz17Uhqt/hwdPRLQZZB4ACKX94H9e\n\
uthNc9goTN3c00xJ39o3fT7o3oDvqYvVitZ2jhblg5DChUDFnt1Hl7hPDlzpvwdB\n\
5GicMFWiOh+Jt+C29L/FdUi3P9NKMsnQOQLg//97u0VTvPHhmhdrjF6YSyMEpo/G\n\
RpXcOjthl0x9EsNWvxiVO94u3t18rSahjGFbUyde47DKXhE1YsWJsQ00scL8Wpv0\n\
O9nHmi2mV9NLNhiOTTraoQfQPUKbPn5+6/1wLBoT3UgsocFZpxww\n\
-----END CERTIFICATE-----";

#define NUM_PIXELS 53
#define DATA_PIN D5

Adafruit_NeoPixel pixels(NUM_PIXELS, DATA_PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500

WiFiClientSecure wclient; // wifi client
PubSubClient client (wclient);
BearSSL::X509List x509(test_sr);

uint32_t current_color = Adafruit_NeoPixel::Color(0,255,0);
RGB m_current = RGB::FromRGB(255, 0, 0);

void setup() {  
  pinMode(BUILTIN_LED, OUTPUT);

  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  
  Serial.print("connecting to ");
  Serial.print(ssid);
  Serial.println("...");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  client.setBufferSize(1024);
  client.setKeepAlive(15);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println('\n');
  Serial.println("connection estabilished");
  Serial.print("IP Adress: \t");
  Serial.println(WiFi.localIP());
  wclient.setInsecure(); 

  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
    clock_prescale_set(clock_div_1);
  #endif

  pixels.begin();
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("attempting MQTT connection...");

    String clientId = "IoT-ESP-12E-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str(), username, devicepassword)) {
      Serial.println("connected");
      
      // 
      if(client.subscribe(commands.c_str(), 1)) {
        Serial.println("subscribed");
      }
      
      String message = "iot-esp 12E connected [";
      message += clientId;
      message += "]";
      
      if(client.publish(commands.c_str(), message.c_str())) {
        Serial.println("published");
      }
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");

  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  int pos = 0;
  String command = "";
  for (int i=0;i<length;i++) {
    if ((char)payload[i] == '=')
      break;
    command += (char)payload[i];
    pos++;
  }

  if (command == "1") {
    digitalWrite(BUILTIN_LED, LOW);   
    setColor(RGB::Black(), m_current);
    return;
  }

  if (command == "0") {
    digitalWrite(BUILTIN_LED, HIGH); 
    setColor(m_current, RGB::Black());
    return;
  }

  if (command == "rgb") {
    int idx = 0;
    uint16_t* map = new uint16_t[3];
    command = "";
    for (int i=pos + 1;i<length;i++) {
      if ((char)payload[i] == ':') {
        map[idx] = (uint16_t)command.toInt();
        command = "";
        idx++;
        continue;
      }

      command += (char)payload[i];  
    }
    map[idx] = (uint16_t)command.toInt();
    RGB color = RGB::FromRGB(map[0],map[1],map[2]);    
    setColor(m_current, color);
    m_current = color;
    return;
  }

  if (command == "brightness") {
    command = "";
    for (int i=pos + 1;i<length;i++) {
      command += (char)payload[i];
    }

    pixels.setBrightness((uint8_t)command.toInt());
    pixels.show();
    return;
  }
}

void setColor(RGB from, RGB to) {
  for (uint8_t i = 0; i < 99; i++) {
      RGB step = Mix(from, to, i, 100);

      for (int i = 0; i < NUM_PIXELS; i++) {
        pixels.setPixelColor(i, step.r, step.g, step.b);
      }
      pixels.show();
      delay(10);
  }

  for (int i = 0; i < NUM_PIXELS; i++) {
    pixels.setPixelColor(i, to.r, to.g, to.b);
  }
  pixels.show();
}
