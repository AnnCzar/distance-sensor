#define trigPin 12
#define echoPin 11
 
void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT); //Pin, do którego podłączymy trig jako wyjście
  pinMode(echoPin, INPUT); //a echo, jako wejście
  pinMode(2, OUTPUT); //Wyjście dla buzzera
}
 
void loop() {  
  zakres(20); //Włącz alarm, jeśli w odległości od 10 do 25 cm od czujnika jest przeszkoda  
  delay(100);
} 
 
int zmierzOdleglosc() {
  long czas, dystans;
 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  czas = pulseIn(echoPin, HIGH);
  dystans = czas / 58;
 
  return dystans;
}
 
void zakres(int a) {
  int jakDaleko = zmierzOdleglosc();
  if (jakDaleko < a) {
      digitalWrite(2, HIGH); //Włączamy buzzer
      Serial.println(jakDaleko); // Wysyłanie odległości na port szeregowy
  } else {
      digitalWrite(2, LOW); //Wyłączamy buzzer, gdy obiekt poza zakresem
      Serial.println(jakDaleko); // Wysyłanie odległości na port szeregowy
  }
}







