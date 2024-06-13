Harvesting data from satellites in range using a GPS sensor like the one I testes with(U-blox M6). 
Reading data directly coming to the sensor via serial ports on Raspberrypi 4 model B, using UART protocol then parsing NMEA sentences over time. 
Separating usefull information depending on the type the sentence we receive. 
THe most crucial part of it is to create Pandas data frame in real time while avoiding any errors related with different situations. To exemplify, 
  - While device is off, waiting to be turned on.
  - When there is no connection(No fix situation).
  - After it's fixed, getting None values from satellites.
    - Then getting started receiving meaningfull sentences again.
  - To ensure data safety, creating a csv file after each loop.
