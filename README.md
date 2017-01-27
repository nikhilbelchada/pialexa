# pialexa
* Dependencies

  sudo apt-get install libasound2-dev

* setup.sh

  Fill in alexa client id, client secret and django secret key
* install requirement.txt
  
  pip install -r requirement.txt
* start server
  
  . setup.sh
  
  python manage.py runserver
 
* Start PiAlexa Service
  
  `python start.py 1`  -> for console version
  `python start.py`  -> For RaspberryPi with SenseHat
