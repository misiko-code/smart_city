//there are many open source code for wemos and dht sensor. This sketch is simple.
#include "DHT.h"
//#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#define DHTPIN 13
#define DHTTYPE DHT11

String sensorId = "123456";

const char* ssid = "TP-Link_8E70";
const char* password = "SummerTU25*";

String host = "192.168.1.255";
String endpoint = "/"+ String(sensorId) + "/value";

DHT dht(DHTPIN, DHTTYPE);
WiFiClient wifiClient;
HTTPClient http;    //Declare object of class HTTPClient
const long utcOffsetInSeconds =3600;
// A UDP instance to let us send and receive packets over UDP
//WiFiUDP ntpUDP;
//NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds); 


void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);//WiFi name and password
  dht.begin(); //start the DHT sensor reader
}

void loop() {
  //while(!timeClient.update()) 
    //{timeClient.forceUpdate();}
  //read the temperature and humidity (temperature sensor specific code)
  float humidity = dht.readHumidity(); //read humidity
  float temperature = dht.readTemperature(); //read temperature (C)
  //String zeit = timeClient.getFormattedTime() ;//read time

  send_to_server(humidity,temperature);

  // check if returns are valid
  /*if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT");
  } else {  //if it read correctly
    Serial.print(humidity);     //humidity
    Serial.print(" \t"); //tab
    Serial.println(temperature);   //temperature (C)
  }*/
  delay(1000);
}

void send_to_server(float t,float h) {
  String postData = "temperature=" + (String)t +"&" + "humidity=" +(String)h;
  
  if (WiFi.status() == WL_CONNECTED) 
  { //Check WiFi connection status
    
	// type your domain name or Node-RED IP address, so the ESP publishes the readings to your own server.
    http.begin(wifiClient, host+endpoint);//if the sensor data do not display in web page, you have to check the status of port 3007. Sometimes the port is not available！
	//Specify content-type header
	http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    
	int httpCode = http.POST(postData);   //Send the request
	
	Serial.println(httpCode);   //Print HTTP return code
    
	http.end();  //Close connection
	
    Serial.println(postData);
  }
  
  else 
  {
    Serial.println("Error in WiFi connection");
  }
  

}
