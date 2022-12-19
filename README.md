# **yandex-iot-core-alice**
Smart home Yandex backend based on Yandex cloud function and ESP8266 (ESP32)

## **Настройка Arduino IDE**
http://arduino.esp8266.com/stable/package_esp8266com_index.json



## **работа с ESP8266 через Yandex IoT Core MQTT**
- создание брокера в yandex cloud
- настройка скетча


### **Device CFG**
В папке со скетчем для Arduino нужно создаться файл `cfg.h`, и в нем прописать нужные параметры
```c
// WiFi client settings.
const char *_ssid = "";     // WiFi SSID.
const char *_password = ""; // WiFi password.
// Yandex CLOUD.
const char *_username = "";         // Yandex IoT broker ID.
const char *_devicepassword = "";   // Yandex IoT broker password.
```

- проверка через Yandex Cli


## **Yandex Cloud Function**

Для бекэнда навыка умного дома в этом проекте используется Yandex Cloud Funtion на языке Python.

### **аторизация через Я.ID**

В отличии от навыков Алисы, навыки умного дома требуют автоизацию по протоколу oauth 2.0. Для личного использвания можно воспользоваться [Я.ID](https://oauth.yandex.ru). 

Переходим, логинимся и создаем новое приложение. Внизу, где раздел **Какие данные вам нужны?** ищем раздел **Умный дом Яндекса • iot** и ставим галочки

```
- Просмотр списка устройств умного дома
- Управление устройствами умного дома
```

### **создание навыка умного дома**

## **Tестирование**

Тестируем