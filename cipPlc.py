from pycomm3 import LogixDriver

# Initialize the driver with the IP address of the PLC
plc = LogixDriver('10.24.252.111')  # Replace with your PLC's IP address

# Open the connection to the PLC
with plc as comm:
    # Get the list of tags from the PLC
    tag_list = comm.get_tag_list()

    # Print the list of tags
    print("Tag List:")
    flag = 1
    for tag in tag_list:
        if flag <30:
            flag+=1
            #print(tag["tag_name"])
    print(comm.read("ETH_REM2:2:I").value["Ch6 Data"])
    #print(comm.read('DO_16_RESERVA').value)
