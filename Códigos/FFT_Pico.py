import machine 
import math
import time 

#-----------------------------FFT Function----------------------------------------------#
def FFT( IN, N, Frequency ) :
  global f_peaks 
  data = [ 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048 ] 
  a    = N  
  c1   = 0 
  f    = 0 
  o    = 0
  x    = 0

  for i in range(12): #Calcula os níveis 
    if (data[i] <= a) :
        o = i
    
    in_ps  = [ 0.0 for _ in range(data[o]) ]  #input for sequencing
    out_r  = [ 0.0 for _ in range(data[o]) ]  #real part of transform
    out_im = [ 0.0 for _ in range(data[o]) ] #imaginory part of transform

    x = 0
    b = 0 
    while b < o: 
        b += 1 
        c1 = data[b]
        f = data[o] / (c1 + c1)
        j = 0 
        while j < c1:
            j += 1 
            x += 1
            in_ps[x] = in_ps[j] + f
    
  i = 0 
  while i < data[o]:
    i += 1 
    if (in_ps[i] < a):
        out_r[i] = IN[in_ps[i]]

    if (in_ps[i] > a):
        out_r[i] = IN[in_ps[i] - a]
    
  


  i10, i11, n1 = 0, 0, 0 
  e, c, s, tr, ti = 0, 0, 0, 0, 0

  i = 0
  while i < o: 
    i += 1 
    i10 = data[i]            # overall values of sine/cosine  :
    i11 = data[o] / data[i + 1] # loop with similar sine cosine:
    e = 360 / data[i + 1]
    e = 0 - e
    n1 = 0

    j = 0
    while j < i10 :
      j += 1 
      c = cosine(e * j)
      s = sine(e * j)
      n1 = j

      k = 0 
      while k < i11: 
        k += 1 
        tr = c * out_r[i10 + n1] - s * out_im[i10 + n1]
        ti = s * out_r[i10 + n1] + c * out_im[i10 + n1]

        out_r[n1 + i10] = out_r[n1] - tr
        out_r[n1] = out_r[n1] + tr

        out_im[n1 + i10] = out_im[n1] - ti
        out_im[n1] = out_im[n1] + ti

        n1 = n1 + i10 + i10


  #---> here onward out_r contains amplitude and our_in conntains frequency (Hz)
  i = 0 
  while i < data[o - 1]:
    i += 1  
    out_r[i] = math.sqrt(out_r[i] * out_r[i] + out_im[i] * out_im[i]) # to  increase the speed delete sqrt
    out_im[i] = i * Frequency / N


  x = 0     # peak detection
  i = 1
  while i < data[o - 1] - 1:
    i += 1
    if (out_r[i] > out_r[i - 1] and out_r[i] > out_r[i + 1]):
        in_ps[x] = i 
        x = x + 1
    

  s = 0
  c = 0
  for i in range(x):
    j = c 
    while j < x: 
        j += 1 
        if (out_r[in_ps[i]] < out_r[in_ps[j]]): 
            s = in_ps[i]
            in_ps[i] = in_ps[j]
            in_ps[j] = s
    
    c = c + 1

  for i in range(5):
    f_peaks[i] = out_im[in_ps[i]]


def sine( i : int ):
  out = 0.0  
  j   = i
  while (j < 0) :
    j = j + 360

  while (j > 360) :
    j = j - 360
  
  if (j > -1   and j < 91) :
    out = sine_data[j]
  
  elif(j > 90  and j < 181) :
    out = sine_data[180 - j]
  
  elif(j > 180 and j < 271) :
    out = -sine_data[j - 180]
  
  elif(j > 270 and j < 361) :
    out = -sine_data[360 - j]
  
  return (out / 255)


def cosine( i : int ):
  out = 0.0 
  j   = i

  while (j < 0) :
    j = j + 360
  
  while (j > 360) :
    j = j - 360
  
  if (j > -1   and j < 91) :
    out = sine_data[90 - j]
  
  elif(j > 90  and j < 181) :
    out = -sine_data[j - 90]
  
  elif(j > 180 and j < 271) :
    out = -sine_data[270 - j]
  
  elif(j > 270 and j < 361) :
    out = sine_data[j - 270]
  
  return (out / 255)


#---------------------------------------------------------------------------#
sine_data = [ 0,
              4,    9,    13,   18,   22,   27,   31,   35,   40,   44,
              49,   53,   57,   62,   66,   70,   75,   79,   83,   87,
              91,   96,   100,  104,  108,  112,  116,  120,  124,  127,
              131,  135,  139,  143,  146,  150,  153,  157,  160,  164,
              167,  171,  174,  177,  180,  183,  186,  189,  192,  195,
              198,  201,  204,  206,  209,  211,  214,  216,  219,  221,
              223,  225,  227,  229,  231,  233,  235,  236,  238,  240,
              241,  243,  244,  245,  246,  247,  248,  249,  250,  251,
              252,  253,  253,  254,  254,  254,  255,  255,  255,  255 ] 

data  = [ 0 for i in range ( 1024 ) ]
f_peaks = [ 0 for i in range( 5 ) ]
frequency = 0.0 
#---------------------------------------------------------------------------#

som = machine.ADC ( machine.Pin( 28, machine.Pin.IN ) ) 

while True: 
  
  t = time.time()
  for i in range(1024): 
    data[i] = som.read_u16()
    time.sleep(0.000001)
  
  
  t = time.time() - t
  t = 1024000000 / t
  FFT( data, 1024, t )
  
  print("Frequencia: ")
  print( t )
  
  for i in range(5):
    print("F{}: {}\tHz".format(i, f_peaks[i]))

  time.sleep(0.5) 


#------------------------------------------------------------------------------------#


'''
#Código fonte / oficial :

//---------------------------------------------------------------------------//
static byte sine_data [91] = {  0,
                                4,    9,    13,   18,   22,   27,   31,   35,   40,   44,
                                49,   53,   57,   62,   66,   70,   75,   79,   83,   87,
                                91,   96,   100,  104,  108,  112,  116,  120,  124,  127,
                                131,  135,  139,  143,  146,  150,  153,  157,  160,  164,
                                167,  171,  174,  177,  180,  183,  186,  189,  192,  195,
                                198,  201,  204,  206,  209,  211,  214,  216,  219,  221,
                                223,  225,  227,  229,  231,  233,  235,  236,  238,  240,
                                241,  243,  244,  245,  246,  247,  248,  249,  250,  251,
                                252,  253,  253,  254,  254,  254,  255,  255,  255,  255
                             };

static int  data [1024];
static float f_peaks[5];     // top 5 frequencies peaks in descending order
static int   frequency ;
//---------------------------------------------------------------------------//

void setup() {
  Serial.begin(250000);
  pinMode( 28, INPUT );
}

void loop() {
  
  unsigned long t = micros();
  for ( byte i = 0; i < 1024; i++) {
    data[i] = analogRead(28);
    delayMicroseconds(1); 
  }
  
  t = micros() - t;
  t = 1024000000 / t;
  FFT( data, 1024, t );
  
  Serial.print("Frequencia: ");
  Serial.println( t );
  
  for ( int i = 0; i < 5; i++) {
    Serial.print("F");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(f_peaks[i]);
    Serial.println("\tHz");
  }
  
  delay(500); 
}

//-----------------------------FFT Function----------------------------------------------//

float FFT(int in[], int N, float Frequency) {
  /*
    Code to perform FFT on arduino,
    setup:
    paste sine_data [91] at top of program [global variable], paste FFT function at end of program
    Term:
    1. in[]     : Data array,
    2. N        : Number of sample (recommended sample size 2,4,8,16,32,64,128...)
    3. Frequency: sampling frequency required as input (Hz)

    If sample size is not in power of 2 it will be clipped to lower side of number.
    i.e, for 150 number of samples, code will consider first 128 sample, remaining sample  will be omitted.
    For Arduino nano, FFT of more than 128 sample not possible due to mamory limitation (64 recomended)
    For higher Number of sample may arise Mamory related issue,
    Code by ABHILASH
    Contact: abhilashpatel121@gmail.com
    Documentation:https://www.instructables.com/member/abhilash_patel/instructables/
    2/3/2021: change data type of N from float to int for >=256 samples
  */

  unsigned int data[13] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048};
  int a, c1, f, o, x;
  a = N;

  for (int i = 0; i < 12; i++)          //calculating the levels
  {
    if (data[i] <= a) {
      o = i;
    }
  }

  int in_ps[data[o]] = {};   //input for sequencing
  float out_r[data[o]] = {}; //real part of transform
  float out_im[data[o]] = {}; //imaginory part of transform

  x = 0;
  for (int b = 0; b < o; b++)              // bit reversal
  {
    c1 = data[b];
    f = data[o] / (c1 + c1);
    for (int j = 0; j < c1; j++)
    {
      x = x + 1;
      in_ps[x] = in_ps[j] + f;
    }
  }


  for (int i = 0; i < data[o]; i++)     // update input array as per bit reverse order
  {
    if (in_ps[i] < a)
    {
      out_r[i] = in[in_ps[i]];
    }
    if (in_ps[i] > a)
    {
      out_r[i] = in[in_ps[i] - a];
    }
  }


  int i10, i11, n1;
  float e, c, s, tr, ti;

  for (int i = 0; i < o; i++)                             //fft
  {
    i10 = data[i];            // overall values of sine/cosine  :
    i11 = data[o] / data[i + 1]; // loop with similar sine cosine:
    e = 360 / data[i + 1];
    e = 0 - e;
    n1 = 0;

    for (int j = 0; j < i10; j++)
    {
      c = cosine(e * j);
      s = sine(e * j);
      n1 = j;

      for (int k = 0; k < i11; k++)
      {
        tr = c * out_r[i10 + n1] - s * out_im[i10 + n1];
        ti = s * out_r[i10 + n1] + c * out_im[i10 + n1];

        out_r[n1 + i10] = out_r[n1] - tr;
        out_r[n1] = out_r[n1] + tr;

        out_im[n1 + i10] = out_im[n1] - ti;
        out_im[n1] = out_im[n1] + ti;

        n1 = n1 + i10 + i10;
      }
    }
  }

  /*
    for(int i=0;i<data[o];i++)
    {
    Serial.print(out_r[i]);
    Serial.print("\t");                                     // un comment to print RAW o/p
    Serial.print(out_im[i]); Serial.println("i");
    }
  */


  //---> here onward out_r contains amplitude and our_in conntains frequency (Hz)
  for (int i = 0; i < data[o - 1]; i++)      // getting amplitude from compex number
  {
    out_r[i] = sqrt(out_r[i] * out_r[i] + out_im[i] * out_im[i]); // to  increase the speed delete sqrt
    out_im[i] = i * Frequency / N;
    /*
      Serial.print(out_im[i]); Serial.print("Hz");
      Serial.print("\t");                            // un comment to print freuency bin
      Serial.println(out_r[i]);
    */
  }




  x = 0;     // peak detection
  for (int i = 1; i < data[o - 1] - 1; i++)
  {
    if (out_r[i] > out_r[i - 1] && out_r[i] > out_r[i + 1])
    { in_ps[x] = i;  //in_ps array used for storage of peak number
      x = x + 1;
    }
  }


  s = 0;
  c = 0;
  for (int i = 0; i < x; i++)      // re arraange as per magnitude
  {
    for (int j = c; j < x; j++)
    {
      if (out_r[in_ps[i]] < out_r[in_ps[j]])
      { s = in_ps[i];
        in_ps[i] = in_ps[j];
        in_ps[j] = s;
      }
    }
    c = c + 1;
  }



  for (int i = 0; i < 5; i++) // updating f_peak array (global variable)with descending order
  {
    f_peaks[i] = out_im[in_ps[i]];
  }



}


float sine(int i)
{
  int j = i;
  float out;
  while (j < 0) {
    j = j + 360;
  }
  while (j > 360) {
    j = j - 360;
  }
  if (j > -1   && j < 91) {
    out = sine_data[j];
  }
  else if (j > 90  && j < 181) {
    out = sine_data[180 - j];
  }
  else if (j > 180 && j < 271) {
    out = -sine_data[j - 180];
  }
  else if (j > 270 && j < 361) {
    out = -sine_data[360 - j];
  }
  return (out / 255);
}

float cosine(int i)
{
  int j = i;
  float out;
  while (j < 0) {
    j = j + 360;
  }
  while (j > 360) {
    j = j - 360;
  }
  if (j > -1   && j < 91) {
    out = sine_data[90 - j];
  }
  else if (j > 90  && j < 181) {
    out = -sine_data[j - 90];
  }
  else if (j > 180 && j < 271) {
    out = -sine_data[270 - j];
  }
  else if (j > 270 && j < 361) {
    out = sine_data[j - 270];
  }
  return (out / 255);
}

//------------------------------------------------------------------------------------//
'''