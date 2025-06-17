
#include <ESP8266WiFi.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESP8266HTTPClient.h>

// WiFi and servercredentials
const char *ssid = "TP-Link_8E70";    // Replace with your WiFi SSID
const char *password = "SummerTU25*"; // Replace with your WiFi password
String host="192.168.1.101:8000"; // Server IP address, listening address of uvicorn 
String api= "/sensors/sensor_data";//fastapi post request url

// API endpoint to send data
String serverUrl = "http://" + host + api; // Complete URL for the API endpoint

// DHT setup
#define DHTPIN D4     // GPIO pin (D4 = GPIO2)
#define DHTTYPE DHT11 // or DHT22
DHT dht(DHTPIN, DHTTYPE);

WiFiClient wifiClient;
HTTPClient http; // Declare object of class HTTPClient

void setup()
{
  Serial.begin(9600);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
}

void loop()
{
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum))
  {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  if (WiFi.status() == WL_CONNECTED)
  {

    http.begin(wifiClient, serverUrl);
    http.addHeader("Content-Type", "application/json");

    String postData = "{\"temperature\":" + String(temp, 2) +
                      ",\"humidity\":" + String(hum, 2) + "}";
    Serial.println("Sending: " + postData);

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0)
    {
      Serial.print("POST Response: ");
      Serial.println(httpResponseCode);
    }
    else
    {
      Serial.print("POST Failed. Error: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();
  }

  delay(100); // Wait 100ms before sending another packet
}
