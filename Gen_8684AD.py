import visa

class Agilent_8684:
    """"Class Agilent_8684, for Agilent 8684A-D Signal Generator.

    Attribute:
        Name(str): name of the signal generator, Model(str): model type of signal generator,
        address_gpib(str): signal generator's GPIB address, freq(str): frequency in MHz

    """

    def __init__(self, name="Signal Generator", model="8648C", address_gpib="19", freq="100",
                 amplitude="-40"):
        self.name = name
        self.model = model
        self.address_gpib = address_gpib
        self.freq = freq
        self.amplitude = amplitude
        self.gpib_socket = None

    def gpib_connect(self):
        """"Establishes a 'socket' with instrument"""
        rm = visa.ResourceManager()
        self.gpib_socket = rm.open_resource("GPIB0::" + self.address_gpib + "::INSTR")
        # self.gpib_socket.write("FREQ:CW 100 MHZ;:POW:AMPL -30 DBM")
        # self.gpib_socket.query("FREQ:CW 100 MHZ;:POW:AMPL -30 DBM;*OPC?")

    def gpib_send(self, gpib_message="*IDN?"):
        """"Connects to GPIB socket and sends GPIB command with message"""
        if gpib_message.find("?") != -1:
            answer = self.gpib_socket.query(gpib_message)
            return answer
        else:
            self.gpib_socket.write(gpib_message)

    def set_default_all(self):
        """"Sets frequency signal generator to LPT default settings: freq 100 MHz, power -40 dBm, RF State On"""
        self.gpib_send("FREQ:CW 100 MHZ;:POW:AMPL -40 DBM;:OUTP:STAT ON")

    def set_rf(self, power="on"):
        """"turns on the RF Output on or off"""
        power = power.lower()
        if power == "on":
            self.gpib_send("OUTP:STAT ON")
        elif power == "off":
            self.gpib_send("OUTP:STAT OFF")

    def set_freq(self, freq_val="100 MHZ"):
        self.gpib_send("FREQ:CW " + freq_val)

    def set_amp(self, amp_val="-40 DBM"):
        """"Sets signal generator to desired amplitude, if over 0 dBm, do not work"""
        test_amp = int(amp_val.strip("dbmDBM"))
        if test_amp < 0:
            self.gpib_send("POW:AMPL " + amp_val)
        else:
            print("value too high")

    def get_freq_amp(self):
        """"Queries frequency and amplitude, turns the values into a float, then returns back as an array"""
        value_return = self.gpib_send("FREQ:CW?;:POW:AMPL?")
        value_return = value_return.split(";")
        float_freq = "{} Hz".format(float(value_return[0]))
        float_amp = "{} dBm".format(float(value_return[1]))
        return float_freq, float_amp