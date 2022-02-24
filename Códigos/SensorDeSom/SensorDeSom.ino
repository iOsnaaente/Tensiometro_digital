#define ANALOG_SOM  28

static int limiar; 

void setup() {
  Serial.begin( 115200 );
  pinMode( ANALOG_SOM, INPUT );
  limiar = calibration( 10000 );
  delay(1000);
  
}


int calibration( int num_count ){
  Serial.println("Calibrando, faça silêncio e deixe apenas o barulho ambiente!");
  long int bank = 0; 
  
  for ( int count = num_count; count > 0; count --  )
    bank += analogRead( ANALOG_SOM );

  limiar = bank/num_count; 
  Serial.print( "Limiar calculado: ");
  Serial.println( limiar );
  
  // Média do valor de leitura do contador
  // Pode ser usado como um limiar de leitura 
  return limiar; 
}


void loop() {
  int amplitude = analogRead( ANALOG_SOM );

  if (Serial.available() ){
    if (Serial.read() == 'C' ){
      limiar = calibration(2500); 
      delay(1000);
    }
  }
  
  if ( (float)amplitude > limiar*1.25 || (float)amplitude < limiar*0.75 )
    digitalWrite( 2, !digitalRead(2) );
  
  Serial.print( "Amplitude: ");
  Serial.println( amplitude ) ;
  
}
