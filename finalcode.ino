#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include "spo2_algorithm.h"

#include <Protocentral_MAX30205.h>

#define PULSE_PIN 36  // ESP32 ADC pin

// Web Part
#include <WiFi.h> // WIFI link
#include <WebServer.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// SSID & Password
const char* ssid = "LAPTOP-26CMEJ7V 4208";		// "E5785_59AB";         /*Enter Your SSID*/
const char* password = "5jT253@7";		// "71595345";        /*Enter Your Password*/


WebServer server(80);  // Object of WebServer(HTTP port, 80 is defult)

//Your Domain name with URL path or IP address with path
String serverName = "http://192.168.1.2:5000/setReads";


// heart pulse ------------------------------
int readsignal = 0;
int threshold = 512;  // You may need to adjust this

unsigned long lastBeatTime = 0;
float bpm = 0;
int beatCount = 0;



// MAX30102 ---------------------------------
MAX30105 particleSensor;
#define MAX_BRIGHTNESS 255

uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data

uint32_t tsLastReport = 0;  //stores the time the last update was sent to the blynk app

int32_t bufferLength; //data length
int32_t spo2; //SPO2 value
int8_t validSPO2; //indicator to show if the SPO2 calculation is valid
int32_t heartRate; //heart rate value calcualated as per Maxim's algorithm
int8_t validHeartRate; //indicator to show if the heart rate calculation is valid

byte pulseLED = 2; //onboard led on esp32 nodemcu
byte readLED = 19; //Blinks with each data read 

long lastBeat = 0; //Time at which the last beat occurred

float beatsPerMinute; //stores the BPM as per custom algorithm
int beatAvg = 0, sp02Avg = 0; //stores the average BPM and SPO2 
float ledBlinkFreq; //stores the frequency to blink the pulseLED

  

// MAX30205 ----------------------------------
MAX30205 tempSensor;



void setup() {
  // Initialize the Serial to communicate with the Serial Monitor.
  Serial.begin(115200);

  // Heart rate setup ---------------------------
  // Configure the PulseSensor object, by assigning our variables to it
  pinMode(PULSE_PIN, INPUT);
  Serial.println("KY-039 Heart Rate Sensor Initialized");


  // Initialize sensor MAX30102 ------------------
  Wire.begin(); // Default: SDA = 21, SCL = 22

  Serial.print("Initializing Pulse Oximeter..");
  
    // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println(F("MAX30105 was not found. Please check wiring/power."));
    while (1);
  }


  /*The following parameters should be tuned to get the best readings for IR and RED LED. 
   *The perfect values varies depending on your power consumption required, accuracy, ambient light, sensor mounting, etc. 
   *Refer Maxim App Notes to understand how to change these values
   *I got the best readings with these values for my setup. Change after going through the app notes.
   */
  byte ledBrightness = 50; //Options: 0=Off to 255=50mA
  byte sampleAverage = 1; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  byte sampleRate = 100; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 69; //Options: 69, 118, 215, 411
  int adcRange = 4096; //Options: 2048, 4096, 8192, 16384
  
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings


  // MAX 30205 -----------------------------
  Serial.println("MAX30205 sensor initialized.");


  // Web part ----------------------------------
  // Web part 
  Serial.println("Try Connecting to ");
  Serial.println(ssid);

  // Connect to your wi-fi modem
  WiFi.mode(WIFI_AP_STA);                  /*Set the WiFi in STA Mode*/
  WiFi.begin(ssid, password);


  // Check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
      delay(5000);
      Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected successfully");
  Serial.print("Got IP: ");   /// Copy this
  Serial.println(WiFi.localIP());  //Copy this how ESP32 IP on serial


  server.on("/heart", HTTP_GET, handleHeart);
  server.on("/temper", HTTP_POST, handleTemp);
  server.on("/spo2", HTTP_GET, handleSpo);

  server.enableCORS();
  server.begin();

  Serial.println("HTTP started");
  delay(2000);                         /*Wait for 2 seconds to read the IP*/
}

// HTML & CSS contents which display on web server
String HTML = "<!DOCTYPE html>\
<html>\
<body>\
<h1>My First Web Server with ESP32 - Station Mode &#128522;</h1>\
</body>\
</html>";

void loop() {
   Serial.print("Got IP: ");   /// Copy this insidee loop
  Serial.println(WiFi.localIP());  //Copy this insidee loop - how ESP32 IP on serial

  String heartRate = getHeartRate();	// return HRate - int
    
  // MAX30102 sensor
  String max30102 = getSensor30102();	// return String HRate + SPO2

  // MAX 30205 sensor
  float temp = getTemper(); // read temperature for every 100ms - float

  // web part
  //HTML = "" + temp + "-" + heartRate + "-" + max30102;
  server.handleClient();

  delay(5000);  // pause for 1 sec to avoid reading sensors frequently to prolong the sensor lifetime
}


void handleHeart() {
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["hrate"] = String(getHeartRate());
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  server.sendHeader("Access-Control-Allow-Origin","*");
  server.sendHeader("Content-Type", "application/json");
  server.send(200, "application/json", jsonString);
  //flashLED();
}


void handleTemp() {
  StaticJsonDocument<200> jsonDoc;
  String temperature = String(getTemper());
  jsonDoc["temper"] = temperature;
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  server.sendHeader("Access-Control-Allow-Origin","*");
  server.sendHeader("Content-Type", "application/json");
  server.send(200, "application/json", jsonString);
  //flashLED();
}


void handleSpo() {
  StaticJsonDocument<200> jsonDoc;
  String spo = getSensor30102();
  jsonDoc["spo"] = String(spo);
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  server.sendHeader("Access-Control-Allow-Origin","*");
  server.sendHeader("Content-Type", "application/json");
  server.send(200, "application/json", jsonString);
  //flashLED();
}

String getHeartRate(){
   readsignal = analogRead(PULSE_PIN);  // Read analog pulse

  unsigned long currentTime = millis();

  // Basic beat detection using threshold
  if (readsignal > threshold) {
    if (currentTime - lastBeatTime > 300) {  // Ignore noise/rebounds
      bpm = 60000.0 / (currentTime - lastBeatTime);
      lastBeatTime = currentTime;

      Serial.print("Beat detected! BPM: ");
      Serial.println(bpm);
    }
  }

  Serial.print("Analog Signal: ");
  Serial.println(readsignal);
  delay(10);
  return String(readsignal);
}

String getSensor30102(){
  bufferLength = 100; //buffer length of 100 stores 4 seconds of samples running at 25sps
  
  //read the first 100 samples, and determine the signal range
  for (byte i = 0 ; i < bufferLength ; i++)
  {
    while (particleSensor.available() == false) //do we have new data?
      particleSensor.check(); //Check the sensor for new data
  
    redBuffer[i] = particleSensor.getIR();
    irBuffer[i] = particleSensor.getRed();
    particleSensor.nextSample(); //We're finished with this sample so move to next sample
  
    Serial.print(F("red: "));
    Serial.print(redBuffer[i], DEC);
    Serial.print(F("\t ir: "));
    Serial.println(irBuffer[i], DEC);
  }
  
  //calculate heart rate and SpO2 after first 100 samples (first 4 seconds of samples)
  maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
  
  //Continuously taking samples from MAX30102.  Heart rate and SpO2 are calculated every 1 second
  while (1)
  {
    //After gathering 25 new samples recalculate HR and SP02
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
    
    Serial.print(beatAvg, DEC);
    
    Serial.print(F("\t HRvalid="));
    Serial.print(validHeartRate, DEC);
    
    Serial.print(F("\t SPO2="));
    Serial.print( sp02Avg , DEC);
    
    Serial.print(F("\t SPO2Valid="));
    Serial.println(validSPO2, DEC);

    //Calculates average SPO2 to display smooth transitions on Blynk App
    if(validSPO2 == 1 && spo2 < 100 && spo2 > 0)
    {
      sp02Avg = (sp02Avg+spo2)/2;
    }
    else
    {
      spo2 = 0;
      sp02Avg = (sp02Avg+spo2)/2;;
    }
    Serial.println(sp02Avg);

    return String(sp02Avg);
 }
}

float getTemper(){
  float temperature = tempSensor.getTemperature();
  Serial.print("Temperature (C): ");
  Serial.println(temperature);
  delay(1000);
  return temperature;
 }
