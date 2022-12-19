#include "cfg.h"
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi client settings
const char *ssid = _ssid;
const char *password = _password;
bool connectdone = false;

// Yandex CLOUD
const char *mqttServer = "mqtt.cloud.yandex.net";
int mqttPort = 8883;
const char *username = _username;             // Yandex IoT broker ID 
const char *devicepassword = _devicepassword;  // Yandex IoT broker password 
// Setup IoT
const String deviceId = "device-iot-node-mcu-01"; // unique device id for cloud function
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


WiFiClientSecure wclient; // wifi client
PubSubClient client (wclient);
BearSSL::X509List x509(test_sr);

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

  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   
  } else {
    digitalWrite(BUILTIN_LED, HIGH); 
  }
}
