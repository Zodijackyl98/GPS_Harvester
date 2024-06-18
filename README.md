Harvesting data from satellites in range using a GPS sensor like the one I tested with(U-blox Neo 6M). 
Reading data directly coming to the sensor via serial ports on Raspberrypi 4 model B, using UART protocol then parsing NMEA sentences over time. 
Separating usefull information depending on the type the sentence we receive. 
THe most crucial part of it is to create Pandas data frame in real time while avoiding any errors related with different situations. To exemplify, 
  - While device is off, waiting to be turned on.
  - When there is no connection(No fix situation).
  - After it's fixed, getting None values from satellites.
    - Then getting started receiving meaningfull sentences again.
  - To ensure data safety, creating a csv file after each loop also it prints out several parameters for each iteration

Only tested with the mentioned sensor but it's already adapted to work with similar types like 7M, N8M etc. Only difference would be small changes in NMEA sentences.
Code also built by using Raspberrypi 4 Model B 8GB version, haven't tried to run with Zero or Pico but since you need to use Numpy and Pandas libraries, I don't think it's capable of working with Pico but the program is not actually depending on them, one can easily adjust it to just write with simple file manipulation functions that are already exist in Python. 

I believe code will run with older versions of Python(3.9.x) but I had encountered issues with 3.10.14 and they were probably about matplotlib library inside my environment, then created fresh venv with python version 3.10.12, now works without an issue. 
  
