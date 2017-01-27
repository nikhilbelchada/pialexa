# pialexa
* Dependencies

  sudo apt-get install libasound2-dev

* setup.sh

  Fill in alexa client id, client secret and django secret key
* install requirement.txt
  
  pip install -r requirement.txt
* start server (Need to be done only once) 
  
  . setup.sh
  
  python manage.py runserver
  GOTO URL: http://localhost:8000/auth, login with amazon, this will set token for you.
  Note: Make sure you whitelist localhost:8000 in alexa developer console web settings tab.
 
* Start PiAlexa Service
  
  `python start.py 1`  -> for console version
  `python start.py`  -> For RaspberryPi with SenseHat
