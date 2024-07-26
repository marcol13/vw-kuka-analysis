from base64 import decodebytes

def get_bit_from_bytes(bytes, bit_number):
        byte_bit = int(bit_number / 8), bit_number % 8

        return int(bool(bytes[byte_bit[0]] & (1<<byte_bit[1])))

def extraction_func(x: object, filename: str, auto_model_bits: list[int] = [944, 945]):
        inputs = decodebytes(bytes(x["Payload"]["DigitalInputs"]["Value"], encoding='utf8'))
        outputs = decodebytes(bytes(x["Payload"]["DigitalOutputs"]["Value"], encoding='utf8'))
        info = decodebytes(bytes(x["Payload"]["Flags"]["Value"], encoding='utf8'))
        wire_cut = get_bit_from_bytes(outputs, 79)
        end_preparation = get_bit_from_bytes(outputs, 77)

        body_model = [get_bit_from_bytes(info, n_bit) for n_bit in auto_model_bits]
        prad_silnik_0 = inputs[167] << 8 | inputs[166]
        prad_silnik_1 = inputs[169] << 8 | inputs[168]

        id = filename.split(".")[0]
        robot = filename.split("_")[0]
        program = filename.split('-')[1]
        return {
                "id": id,
                "robot": robot,
                "program": program,
                "timestamp": x['Timestamp'],
                "given_laser_power": x["Payload"]["ANOUT"]["Value"][6],
                "given_wire_speed": x["Payload"]["ANOUT"]["Value"][2],
                "real_wire_speed": x["Payload"]["ANIN"]["Value"][2],
                "wire_cut": wire_cut,
                "preparation_end": end_preparation,
                "model": body_model,
                "binzel_motor_0_current": prad_silnik_0,
                "binzel_motor_1_current": prad_silnik_1,
                "scansonic_head_angle": x["Payload"]["ANIN"]["Value"][12],
                "scansonic_tip_depth": x["Payload"]["ANIN"]["Value"][13]
            }
        