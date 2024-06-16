import socket
import struct
import threading
import time
from enum import Enum

class QOI(Enum):
    STATION_INTERROGATION = 0x14
    GROUP_1_INTERROGATION = 0x15
    GROUP_2_INTERROGATION = 0x16
    GROUP_3_INTERROGATION = 0x17
    GROUP_4_INTERROGATION = 0x18
    GROUP_5_INTERROGATION = 0x19
    GROUP_6_INTERROGATION = 0x1A
    GROUP_7_INTERROGATION = 0x1B
    GROUP_8_INTERROGATION = 0x1C
    GROUP_9_INTERROGATION = 0x1D
    GROUP_10_INTERROGATION = 0x1E
    GROUP_11_INTERROGATION = 0x1F
    GROUP_12_INTERROGATION = 0x20
    GROUP_13_INTERROGATION = 0x21
    GROUP_14_INTERROGATION = 0x22
    GROUP_15_INTERROGATION = 0x23
    GROUP_16_INTERROGATION = 0x24

class TypeID(Enum):
    M_SP_NA_1 = (1, "Single-point information")
    M_SP_TB_1 = (2, "Single-point information with time tag")
    M_DP_NA_1 = (3, "Double-point information")
    M_DP_TB_1 = (4, "Double-point information with time tag")
    M_ST_NA_1 = (5, "Step position information")
    M_ST_TB_1 = (6, "Step position information with time tag")
    M_BO_NA_1 = (7, "Bitstring of 32 bit")
    M_BO_TB_1 = (8, "Bitstring of 32 bit with time tag")
    M_ME_NA_1 = (9, "Measured value, normalized value")
    M_ME_TB_1 = (10, "Measured value, normalized value with time tag")
    M_ME_NB_1 = (11, "Measured value, scaled value")
    M_ME_TC_1 = (12, "Measured value, scaled value with time tag")
    M_ME_NC_1 = (13, "Measured value, short floating point value")
    M_ME_TD_1 = (14, "Measured value, short floating point value with time tag")
    M_IT_NA_1 = (15, "Integrated totals")
    M_IT_TB_1 = (16, "Integrated totals with time tag")
    M_EP_TA_1 = (17, "Event of protection equipment with time tag")
    M_EP_TB_1 = (18, "Packed start events of protection equipment with time tag")
    M_EP_TC_1 = (19, "Packed output circuit information of protection equipment with time tag")
    C_SC_NA_1 = (45, "Single command")
    C_DC_NA_1 = (46, "Double command")
    C_RC_NA_1 = (47, "Regulating step command")
    C_SE_NA_1 = (48, "Set-point command, normalized value")
    C_SE_NB_1 = (49, "Set-point command, scaled value")
    C_SE_NC_1 = (50, "Set-point command, short floating point value")
    C_BO_NA_1 = (51, "Bitstring of 32 bit")
    M_EI_NA_1 = (70, "End of initialization")
    C_IC_NA_1 = (100, "Interrogation command")
    C_CI_NA_1 = (101, "Counter interrogation command")
    C_RD_NA_1 = (102, "Read command")
    C_CS_NA_1 = (103, "Clock synchronization command")
    C_TS_TA_1 = (104, "Test command with time tag")
    C_RP_NA_1 = (105, "Reset process command")
    C_CD_NA_1 = (106, "Delay acquisition command")
    P_ME_NA_1 = (110, "Parameter of measured value, normalized value")
    P_ME_NB_1 = (111, "Parameter of measured value, scaled value")
    P_ME_NC_1 = (112, "Parameter of measured value, short floating point value")
    P_AC_NA_1 = (113, "Parameter activation")

    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

class COT(Enum):
    PERIODIC = (1, "Periodic, background scan")
    BACKGROUND = (2, "Background scan")
    SPONTANEOUS = (3, "Spontaneous")
    INITIALIZATION = (4, "Initialization")
    REQUEST = (5, "Request")
    ACTIVATION = (6, "Activation")
    ACTIVATION_CONFIRMATION = (7, "Activation confirmation")
    DEACTIVATION = (8, "Deactivation")
    DEACTIVATION_CONFIRMATION = (9, "Deactivation confirmation")
    ACTIVATION_TERMINATION = (10, "Activation termination")
    RETURN_INFORMATION = (20, "Return information")
    FILE_TRANSFER = (21, "File transfer")
    INTERROGATED_BY_STATION = (30, "Interrogated by station")
    INTERROGATED_BY_GROUP_1 = (31, "Interrogated by group 1")
    INTERROGATED_BY_GROUP_2 = (32, "Interrogated by group 2")
    INTERROGATED_BY_GROUP_3 = (33, "Interrogated by group 3")
    INTERROGATED_BY_GROUP_4 = (34, "Interrogated by group 4")
    INTERROGATED_BY_GROUP_5 = (35, "Interrogated by group 5")
    INTERROGATED_BY_GROUP_6 = (36, "Interrogated by group 6")
    INTERROGATED_BY_GROUP_7 = (37, "Interrogated by group 7")
    INTERROGATED_BY_GROUP_8 = (38, "Interrogated by group 8")
    INTERROGATED_BY_GROUP_9 = (39, "Interrogated by group 9")
    INTERROGATED_BY_GROUP_10 = (40, "Interrogated by group 10")
    INTERROGATED_BY_GROUP_11 = (41, "Interrogated by group 11")
    INTERROGATED_BY_GROUP_12 = (42, "Interrogated by group 12")
    INTERROGATED_BY_GROUP_13 = (43, "Interrogated by group 13")
    INTERROGATED_BY_GROUP_14 = (44, "Interrogated by group 14")
    INTERROGATED_BY_GROUP_15 = (45, "Interrogated by group 15")
    INTERROGATED_BY_GROUP_16 = (46, "Interrogated by group 16")
    INTERROGATED_BY_GROUP_17 = (47, "Interrogated by group 17")
    INTERROGATED_BY_GROUP_18 = (48, "Interrogated by group 18")
    INTERROGATED_BY_GROUP_19 = (49, "Interrogated by group 19")
    INTERROGATED_BY_GROUP_20 = (50, "Interrogated by group 20")
    INTERROGATED_BY_GROUP_21 = (51, "Interrogated by group 21")
    INTERROGATED_BY_GROUP_22 = (52, "Interrogated by group 22")
    INTERROGATED_BY_GROUP_23 = (53, "Interrogated by group 23")
    INTERROGATED_BY_GROUP_24 = (54, "Interrogated by group 24")
    INTERROGATED_BY_GROUP_25 = (55, "Interrogated by group 25")
    INTERROGATED_BY_GROUP_26 = (56, "Interrogated by group 26")
    INTERROGATED_BY_GROUP_27 = (57, "Interrogated by group 27")
    INTERROGATED_BY_GROUP_28 = (58, "Interrogated by group 28")
    INTERROGATED_BY_GROUP_29 = (59, "Interrogated by group 29")
    INTERROGATED_BY_GROUP_30 = (60, "Interrogated by group 30")
    INTERROGATED_BY_GROUP_31 = (61, "Interrogated by group 31")
    INTERROGATED_BY_GROUP_32 = (62, "Interrogated by group 32")

    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

def bytes_to_hex(byte_data):
    return ' '.join(f'{byte:02X}' for byte in byte_data)

def receive_apdu(sock):
    try:
        start_byte = sock.recv(1)
        if not start_byte:
            return None
        if start_byte == b'\x68':
            length_byte = sock.recv(1)
            if not length_byte:
                return None
            length = struct.unpack('B', length_byte)[0]
            apdu = sock.recv(length)
            if len(apdu) != length:
                return None
            full_apdu = start_byte + length_byte + apdu
            return full_apdu
        else:
            return None
    except Exception as e:
        print(f"Error receiving APDU: {e}")
        return None

def parse_apdu(apdu):
    if len(apdu) < 6:
        raise ValueError("APDU too short to contain necessary fields")

    if apdu[0] != 0x68:
        raise ValueError("Invalid start byte")

    length = apdu[1]
    control_field = apdu[2:6]
    asdu = apdu[6:6+length-4]

    return {
        'length': length,
        'control_field': control_field,
        'asdu': asdu
    }

def parse_control_field(control_field):
    if len(control_field) != 4:
        raise ValueError("Control field must be 4 bytes long")

    send_seq_num = struct.unpack('<H', control_field[:2])[0] >> 1
    receive_seq_num = struct.unpack('<H', control_field[2:4])[0] >> 1

    return {
        'send_seq_num': send_seq_num,
        'receive_seq_num': receive_seq_num
    }

def parse_asdu(asdu):
    if len(asdu) == 0:
        raise ValueError("Empty Frame..")
    if len(asdu) < 8:
        raise ValueError("ASDU too short to contain necessary fields")

    type_id = asdu[0]
    vsq = asdu[1]
    cot = struct.unpack('B', asdu[2:3])[0]
    addr = struct.unpack('<H', asdu[3:5])[0]
    ioa = struct.unpack('<I', asdu[5:8] + b'\x00')[0]

    data = asdu[8:]
    
    return {
        'type_id': type_id,
        'vsq': vsq,
        'cot': cot,
        'addr': addr,
        'ioa': ioa,
        'data': data
    }

def parse_vsq(vsq_byte):
    number_of_objects = vsq_byte & 0x7F
    is_continuous = (vsq_byte & 0x80) >> 7
    return {
        'number_of_objects': number_of_objects,
        'is_continuous': bool(is_continuous)
    }

def parse_iec_104_i_frame(frame):
    frame_bytes = frame
    if len(frame_bytes) < 12:
        raise ValueError("Invalid frame length")

    start_frame = frame_bytes[0]
    apdu_length = frame_bytes[1]
    control_field_1 = frame_bytes[2:4]
    control_field_2 = frame_bytes[4:6]
    asdu_data = frame_bytes[6:6 + apdu_length - 2]

    type_id = asdu_data[0]
    vsq = parse_vsq(asdu_data[1])
    cot = asdu_data[2:4]
    common_address = asdu_data[4:6]
    common_address_value = int.from_bytes(common_address, byteorder='little')

    if common_address_value == 0xFFFF:
        common_address_description = "Unspecified or reserved address"
    else:
        common_address_description = f"Address {common_address_value}"

    information_objects = asdu_data[6:]

    decoded_objects = decode_information_objects(information_objects)

    return {
        'start_frame': start_frame,
        'apdu_length': apdu_length,
        'control_field_1': control_field_1,
        'control_field_2': control_field_2,
        'type_id': type_id,
        'vsq': vsq,
        'cot': cot,
        'common_address': common_address_description,
        'information_objects': decoded_objects
    }

def decode_information_objects(data):
    objects = []
    index = 0
    while index < len(data):
        if index + 4 > len(data):
            break
        obj_address = int.from_bytes(data[index:index+3], byteorder='little')
        qoi = data[index+3]
        qoi_enum = QOI(qoi) if qoi in QOI._value2member_map_ else qoi
        objects.append({
            'obj_address': obj_address,
            'qoi': qoi_enum
        })
        index += 4
    return objects

def process_frames(frames):
    results = []
    for frame in frames:
        try:
            parsed_frame = parse_iec_104_i_frame(frame)
            type_id_enum = TypeID(parsed_frame['type_id']) if parsed_frame['type_id'] in TypeID._value2member_map_ else parsed_frame['type_id']
            cot_enum = COT(int.from_bytes(parsed_frame['cot'], byteorder='little')) if int.from_bytes(parsed_frame['cot'], byteorder='little') in COT._value2member_map_ else parsed_frame['cot']
            results.append({
                'Type ID': type_id_enum.description if isinstance(type_id_enum, TypeID) else type_id_enum,
                'VSQ': parsed_frame['vsq'],
                'Cause of Transmission': cot_enum.description if isinstance(cot_enum, COT) else cot_enum,
                'Common Address': parsed_frame['common_address'],
                'Information Objects': parsed_frame['information_objects']
            })
        except ValueError as e:
            results.append(f"Error: {e}")
    return results

def get_value_from_asdu(type_id, data):
    if type_id == 1:
        if len(data) < 1:
            raise ValueError("Data too short for Single point information")
        value = struct.unpack('B', data[:1])[0]
    elif type_id == 3:
        if len(data) < 1:
            raise ValueError("Data too short for Double point information")
        value = struct.unpack('B', data[:1])[0]
    elif type_id == 9:
        if len(data) < 2:
            raise ValueError("Data too short for Measured value, normalized")
        value = struct.unpack('<h', data[:2])[0] / 32767.0
    elif type_id == 36:
        if len(data) < 4:
            raise ValueError("Data too short for Measured value, short floating point")
        value = struct.unpack('<f', data[:4])[0]
    elif type_id == 45:
        if len(data) < 1:
            raise ValueError("Data too short for Single command")
        value = struct.unpack('B', data[:1])[0]
    elif type_id == 50:
        if len(data) < 6:
            raise ValueError("Data too short for Scaled Value Command")
        qualifier = data[0]
        short_float_value_bytes = data[1:5]
        short_float_value = struct.unpack('<f', short_float_value_bytes)[0]
        value = {
            'qualifier': qualifier,
            'short_float_value': short_float_value
        }
    else:
        value = None

    return value

def create_i_frame(send_seq_num, receive_seq_num, asdu):
    start_byte = b'\x68'
    control_field = struct.pack('<H', send_seq_num << 1) + struct.pack('<H', receive_seq_num << 1)
    length = struct.pack('B', 4 + len(asdu))
    return start_byte + length + control_field + asdu

def create_s_frame(receive_seq_num):
    start_byte = b'\x68'
    length = b'\x04'
    control_field = struct.pack('<H', receive_seq_num << 1) + b'\x01\x00'
    return start_byte + length + control_field

def create_u_frame(start_act=False, start_con=False, stop_act=False, stop_con=False, test_act=False, test_con=False):
    start_byte = b'\x68'
    length = b'\x04'
    if start_act:
        control_field = b'\x07\x00\x00\x00'
    elif start_con:
        control_field = b'\x0B\x00\x00\x00'
    elif stop_act:
        control_field = b'\x13\x00\x00\x00'
    elif stop_con:
        control_field = b'\x23\x00\x00\x00'
    elif test_act:
        control_field = b'\x43\x00\x00\x00'
    elif test_con:
        control_field = b'\x83\x00\x00\x00'
    else:
        control_field = b'\x00\x00\x00\x00'
    return start_byte + length + control_field

# Add functions to handle S-frames and U-frames
def is_s_frame(control_field):
    return (control_field[0] & 0x03) == 0x01

def is_u_frame(control_field):
    return (control_field[0] & 0x03) == 0x03

def handle_client(conn, addr):
    send_seq_num = 0
    receive_seq_num = 0

    print(f"Connected by {addr}")

    try:
        while True:
            apdu = receive_apdu(conn)
            if apdu is None:
                break

            parsed_apdu = parse_apdu(apdu)
            control_field = parsed_apdu['control_field']
            asdu = parsed_apdu['asdu']
            control_info = parse_control_field(control_field)

            if is_s_frame(control_field):
                # Handle S-frame (send acknowledgement)
                print(f"S-frame received control Field {bytes_to_hex(control_field)} || APDU -> {bytes_to_hex(apdu)}")
                receive_seq_num = control_info['receive_seq_num']
                s_frame = create_s_frame(receive_seq_num)
                conn.sendall(s_frame)
            elif is_u_frame(control_field):
                # Handle U-frame (control commands)
                print(f"U-frame received control Field {bytes_to_hex(control_field)} || APDU -> {bytes_to_hex(apdu)}")
                if control_field == b'\x07\x00\x00\x00':  # STARTDT ACT
                    print("STARTDT ACT received.")
                    u_frame = create_u_frame(start_con=True)
                    conn.sendall(u_frame)
                elif control_field == b'\x13\x00\x00\x00':  # STOPDT ACT
                    print("STOPDT ACT received.")
                    u_frame = create_u_frame(stop_con=True)
                    conn.sendall(u_frame)
                elif control_field == b'\x43\x00\x00\x00':  # TESTFR ACT
                    print("TESTFR ACT received.")
                    u_frame = create_u_frame(test_con=True)
                    conn.sendall(u_frame)
            else:
                print(f"I-frame received control Field {bytes_to_hex(control_field)} || APDU -> {bytes_to_hex(apdu)}")
                apdu_info = parse_apdu(apdu)
                control_info = parse_control_field(apdu_info['control_field'])
                
                # value = get_value_from_asdu(asdu['type_id'], asdu['data'])
                
                # Increment the receive sequence number for each valid I-frame
                receive_seq_num = (receive_seq_num + 1) % 32768
                
                # Send I-frame as acknowledgment with the same ASDU payload
                i_frame = create_i_frame(send_seq_num, receive_seq_num, asdu)
                conn.sendall(i_frame)
                # bytes_sent += len(i_frame)
                
                # Increment the send sequence number
                send_seq_num = (send_seq_num + 1) % 32768

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        print(f"Disconnected from {addr}")

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

# Start the server
start_server('192.168.126.1', 2404)
