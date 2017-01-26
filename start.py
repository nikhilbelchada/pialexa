from sensehat_helper import SenseHatHelper

if __name__ == "__main__":
    sense_object = SenseHatHelper()
    print "Welcome to PiAlexa AI!!! Ask any question by pressing SenseHAT middle button!!"
    sense_object.sense_hat.show_letter("?")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        sense_object.sense_hat.clear()
        print "Hope you enjoyed!!!!"    
