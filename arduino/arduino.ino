/*

Projeto 1 - Termostato
IE327Q - 2 Semestre 2017

Professor Dr. Fabiano Fruett

Alunos:  Euclides
         Mathias
         Talles

*/

/* Pinos a serem utilizados no projeto */
#define pinoSensor 0
#define pinoAlarme 12
#define pinoAtuador 13

void setup() 
{ 
  /* Inicializa comunicacao serial a 9600 bps */  
  Serial.begin(9600);
  
  /* Configura pinos do alarme e atuador(aquecedor) como saida */
  pinMode(pinoAlarme, OUTPUT);
  pinMode(pinoAtuador, OUTPUT);  
}

/* Rotina que realiza a leitura dos dados via serial */
String leSerial()
{
  /* Variavel que armazena recepçao da comunicaçao serial */
  String leitura = "";
  /* Variavel auxiliar para leitura serial */  
  char caracter; 
  
  /* Ha dados a serem recepcionados? */
  while(Serial.available() > 0) 
  {
    /* Armazena o valor caso seja diferente de '\n' */
    caracter = Serial.read(); 
    if (caracter != '\n')
      leitura.concat(caracter);
  }
  
  /* Retorna a string lida via serial */
  return leitura; 
}

void loop() {
  
  /* Inicializa variavel auxiliar de leitura serial */
  String leituraSerial = "";
  
  /* Amostra o canal do termistor */  
  int leituraTermistor = analogRead(pinoSensor);
  
  /* Envia valor amostrado via serial */
  Serial.println(leituraTermistor);   
  
  /* Ha dados a serem recepcionados? */
  if (Serial.available() > 0)
  {
    /* Realiza a leitura serial */
    leituraSerial = leSerial();
    
    /* Se o primeiro caracter do pacote recebido for 0, desliga o alarme. Caso contrario o liga */
    (leituraSerial.charAt(0)=='0') ? (digitalWrite(pinoAlarme, LOW)) : (digitalWrite(pinoAlarme, HIGH));
    /* Se o segundo caracter do pacote recebido for 0, desliga o atuador. Caso contrario o liga */
    (leituraSerial.charAt(1)=='0') ? (digitalWrite(pinoAtuador, LOW)) : (digitalWrite(pinoAtuador, HIGH));    
  }
  
  /* Espera intervado de 500ms */
  delay(500); 
}
