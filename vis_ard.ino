#include "BluetoothSerial.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#define PIN_PINKY     13
#define PIN_RING      12
#define PIN_MIDDLE    14
#define PIN_INDEX     27
#define PIN_THUMB     26
Adafruit_MPU6050 mpu;
BluetoothSerial SerialBT;
void setup(void) {
  Serial.begin(9600);
  SerialBT.begin("Cosmic Claw 2"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  //Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  
  //Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  //Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    //Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    //Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    //Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    //Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  //Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    //Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    //Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    //Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    //Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  //Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    //Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    //Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    //Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    //Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    //Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    //Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    //Serial.println("5 Hz");
    break;
  }

  //Serial.println("");
  delay(100);
}
void loop() {
  int thumb_v= analogRead(PIN_THUMB);
  int index_v= analogRead(PIN_INDEX);
  int middle_v= analogRead(PIN_MIDDLE );
  int ring_v= analogRead(PIN_RING);
  int pinky_v= analogRead(PIN_PINKY );
  
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  /* ax,ay,az,gx,gy,gz,temp,thumb,index,middle,ring,pinky*/
 
  Serial.print(a.acceleration.x);
  Serial.print(",");
  Serial.print(a.acceleration.y);
  Serial.print(",");
  Serial.print(a.acceleration.z);
  Serial.print(","); 
  Serial.print(g.gyro.x);
  Serial.print(",");
  Serial.print(g.gyro.y);
  Serial.print(",");
  Serial.print(g.gyro.z);
  Serial.print(",");
  Serial.print(temp.temperature);
  Serial.print(",");
  Serial.print(thumb_v);
  Serial.print(",");
  Serial.print(index_v);
  Serial.print(",");
  Serial.print(middle_v);
  Serial.print(",");
  Serial.print(ring_v);
  Serial.print(",");
  Serial.print(pinky_v);
  Serial.println();
  
    /*SerialBT.print(a.acceleration.x);
    SerialBT.print(",");
    SerialBT.print(a.acceleration.y);
    SerialBT.print(",");
    SerialBT.print(a.acceleration.z);
    SerialBT.print(","); 
    SerialBT.print(g.gyro.x);
    SerialBT.print(",");
    SerialBT.print(g.gyro.y);
    SerialBT.print(",");
    SerialBT.print(g.gyro.z);
    SerialBT.print(",");
    SerialBT.print(temp.temperature);
    SerialBT.print(",");*/
    SerialBT.print(thumb_v);
    SerialBT.print(",");
    SerialBT.print(index_v);
    SerialBT.print(",");
    SerialBT.print(middle_v);
    SerialBT.print(",");
    SerialBT.print(ring_v);
    SerialBT.print(",");
    SerialBT.print(pinky_v);
    SerialBT.print("\n");
 
  delay(50);
}
