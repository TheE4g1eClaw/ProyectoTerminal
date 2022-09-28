#include <wiringPi.h>
#include <unistd.h>

/* Pocisiones de los motores en el registro de control */
#define MOTOR1_A 2
#define MOTOR1_B 3
#define MOTOR2_A 1
#define MOTOR2_B 4
#define MOTOR4_A 0
#define MOTOR4_B 6
#define MOTOR3_A 5
#define MOTOR3_B 7

/* Pines para configurar el registro de control */
#define R_LATCH 18
#define R_CLOCK 23
#define R_ENABLE 24
#define R_DATA 8

//#define PWM_M1
#define PWM_M2 7
#define PWM_M3 25
//#define PWM_M4

char estado; //arreglo de 8 bits
//int velocidad;

void estadoARegistro();
void adelante();
void atras();
void izquierda();
void derecha();
void parar();
char _BV(char bits);


int main(){
	wiringPiSetupGpio() ;
	
	pinMode(R_LATCH, OUTPUT);
	pinMode(R_ENABLE, OUTPUT);
	pinMode(R_DATA, OUTPUT);
	pinMode(R_CLOCK, OUTPUT);
	
	pinMode(PWM_M2, OUTPUT);
	pinMode(PWM_M3, OUTPUT);
	
	estado = 0;
	estadoARegistro();
	
	while(1){
		digitalWrite(PWM_M2, 1);
		digitalWrite(PWM_M3, 1);
		usleep(50);
		digitalWrite(PWM_M2, 0);
		digitalWrite(PWM_M3, 0);
		usleep(50);
		//analogWrite(PWM_M2, 50);
	}
}

void estadoARegistro(){
  int i;
  
  digitalWrite(R_LATCH, LOW);
  digitalWrite(R_DATA, LOW);

  for (i=0; i<8; i++) {
    digitalWrite(R_CLOCK, LOW);

    if (estado & _BV(7-i)) {
      digitalWrite(R_DATA, HIGH);
    }
    else {
      digitalWrite(R_DATA, LOW);
    }
    digitalWrite(R_CLOCK, HIGH);
  }
  digitalWrite(R_LATCH, HIGH);
}

void adelante(){
  /* Se necesita encender motor 2a y 3a*/
  estado = 0 | _BV(MOTOR2_A) | _BV(MOTOR3_A);
  estadoARegistro();
}

void atras(){
  /* Se necesita encender motor 2b y 3b*/
  estado = 0 | _BV(MOTOR2_B) | _BV(MOTOR3_B);
  estadoARegistro();
}

void parar(){
  estado = 0;
  estadoARegistro();
}

void izquierda(){
  /* Se necesita encender motor 2x y 3x*/ 
  estado = 0 | _BV(1);
  estadoARegistro();
}

void derecha(){
  /* Se necesita encender motor 2x y 3x*/
  estado = 0 | _BV(5);
  estadoARegistro();
}

char _BV(char  bits){
	return 1 << bits;
}
