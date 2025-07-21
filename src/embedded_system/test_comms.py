import comms_module
import time

if __name__ == "__main__":
    esp_port = comms_module.find_esp_port()
    
    
    if(esp_port != -1):
        my_esp = comms_module.initialize_connection(esp_port)
        
        for i in range(6): # 0 -> 5
            print("---------------------------------")
            if comms_module.send_command(my_esp, i): # send <i> finger count to my_esp
                print("Value", i , "sent successfully")
            else:
                print("Sent value Failed:", i)

            A = input("Press any key to continue...")

        time.sleep(2)
        print("---------------------------------")
        if comms_module.send_command(my_esp, 9): # send <i> finger count to my_esp
            print("Value", 9 , "sent successfully")
        else:
            print("Sent value Failed:", 9)

        comms_module.close_connection(my_esp)
    else:
        print("NO ESP Found")


    print("Terminal Close in 5 secs")
    time.sleep(5)

    exit()


