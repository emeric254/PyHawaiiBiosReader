# -*- coding: utf-8 -*-

from pprint import pprint
from tools import BytesReader, BytesWriter


class TongaBios:

    def __init__(self, rom: bytes):
        self.rom = rom
        self.data = {
            'Overview': [],
            'Power table': [],
            'Voltage table 2': [],
            'Voltage table 3': [],
            'Power table': [],
            'GPU freq table': [],
            'MEM freq table': [],
            'Fan table': [],
        }

        self.powerTablepattern = (0x02, 0x07, 0x01, 0x00)
        self.voltageInfopattern = (0x00, 0x03, 0x01, 0x01, 0x07)

        self.fanTableOffset = 559
        self.tdcLimitOffset = 613
        self.powerDeliveryLimitOffset = 31

        self.voltageTable3countOffset = 178
        self.voltageTable3Offset = 179

        self.voltageTable2countOffset = 120
        self.voltageTable2Offset = 121

        self.memoryFrequencyTableCountOffset = 334
        self.memoryFrequencyTableOffset = 342

        self.gpuFrequencyTableCountOffset = 240  # TODO dunno ?
        self.gpuFrequencyTableOffset = 248

        self.tdpLimitOffset = 0
        self.VCELimitTableOffset = 0
        self.AMUAndACPLimitTableOffset = 0
        self.UVDLimitTableOffset = 0

        self.parse_all()

    def calculate_checksum(self):
        oldchecksum = BytesReader.read_int8(self.rom, 33)
        size = BytesReader.read_int8(self.rom, 2) * 512

        newchecksum = oldchecksum - sum(BytesReader.read_int8(self.rom, i) for i in range(size)) % 256

        if oldchecksum == newchecksum:
            print('checksum ok')
        else:
            print('wrong checksum')

        BytesWriter.write_int8(self.rom, 33, newchecksum)
        print('checksum saved')

    def find_pattern(self, pattern: tuple):  # TODO check that
        for i in range(len(self.rom) - len(pattern)):
            buf = []
            for j in range(len(pattern)):
                buf.append(BytesReader.read_int8(self.rom, i + j))
            if tuple(buf) == pattern:
                return i - 1  # TODO this -1 seems odd

    def find_powertable_pattern(self):
        return self.find_pattern(self.powerTablepattern)

    def find_voltageinfo_pattern(self):
        return self.find_pattern(self.voltageInfopattern)

    def parse_positions(self):
        self.voltageInfoPosition = self.find_voltageinfo_pattern()
        print('voltageInfoPosition :', hex(self.voltageInfoPosition))

        self.powerTablePosition = self.find_powertable_pattern()
        print('powerTablePosition :', hex(self.powerTablePosition))

        if self.powerTablePosition is not None:
            self.powerTableSize = BytesReader.read_int8(self.rom, self.powerTablePosition) + 256 * BytesReader.read_int8(self.rom, self.powerTablePosition + 1)
            print('powerTableSize :', hex(self.powerTableSize))
            if self.powerTableSize == 635:
                self.fanTableOffset = 533
            self.fanTablePosition = self.powerTablePosition + self.fanTableOffset

    def parse_overview(self):

        self.pos_biosName = 220
        self.data['Overview'].append({
            'name': 'bios name',
            'value': BytesReader.read_str(self.rom, self.pos_biosName, 32),
            'unit': '',
            'position': str(hex(self.pos_biosName)),
            'length' : '32 char'
        })

    def parse_powertable(self):

        if self.powerTablePosition is not None:

            self.data['Power table'].append({
                'name': 'Power table size',
                'value': str(self.powerTableSize),
                'unit': '',
                'position': '',
                'length' : ''
            })

            if self.powerTableSize in (659, 661):
                value = 'R9 380 (' + str(self.powerTableSize) + ')'
            elif self.powerTableSize in (635,):
                value = 'R9 285 (' + str(self.powerTableSize) + ')'
            else:
                value = 'unknow (' + str(self.powerTableSize) + ')'

            self.data['Power table'].append({
                'name': 'GPU power table type',
                'value': value,
                'unit': '',
                'position': '',
                'length' : ''
            })

            self.data['Power table'].append({
                'name': 'Power limit',  # TODO check that
                'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset)),
                'unit': '%',
                'position': str(hex(self.powerTablePosition + self.powerDeliveryLimitOffset)),
                'length' : '16 bits'
            })

            self.data['Power table'].append({
                'name': 'GPU max clock',  # TODO check that
                'value': str(BytesReader.read_int24(self.rom, self.powerTablePosition + 23)),
                'unit': 'MHz',
                'position': str(hex(self.powerTablePosition + 23)),
                'length' : '24 bits'
            })

            self.data['Power table'].append({
                'name': 'MEM max clock',  # TODO check that
                'value': str(BytesReader.read_int24(self.rom, self.powerTablePosition + 27)),
                'unit': 'MHz',
                'position': str(hex(self.powerTablePosition + 27)),
                'length' : '24 bits'
            })

    def parse_voltagetable(self):
        if self.powerTablePosition:
            self.voltageTable2count = BytesReader.read_int8(self.rom, self.powerTablePosition + self.voltageTable2countOffset)

            self.data['Voltage table 2'].append({
                'name': 'table count',
                'value': str(self.voltageTable2count),
                'unit': '',
                'position': str(hex(self.powerTablePosition)),
                'length' : ''
            })

            self.fullvoltageTable2Offset = self.powerTablePosition + self.voltageTable2Offset

            self.data['Voltage table 2'].append({
                'name': 'table offset',
                'value': str(hex(self.fullvoltageTable2Offset)),
                'unit': '',
                'position': str(hex(self.powerTablePosition + self.voltageTable2Offset)),
                'length' : ''
            })

            for voltage_counter in range(self.voltageTable2count):
                pos_voltage = self.fullvoltageTable2Offset + voltage_counter * 8
                self.data['Voltage table 2'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 1',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })
                pos_voltage += 2
                self.data['Voltage table 2'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 2',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })
                pos_voltage += 2
                self.data['Voltage table 2'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 3',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })
                pos_voltage += 2
                self.data['Voltage table 2'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 4',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })

            self.voltageTable3count = BytesReader.read_int8(self.rom, self.powerTablePosition + self.voltageTable3countOffset)

            self.data['Voltage table 3'].append({
                'name': 'table count',
                'value': str(self.voltageTable3count),
                'unit': '',
                'position': str(hex(self.powerTablePosition + self.voltageTable3countOffset)),
                'length' : ''
            })

            self.fullvoltageTable3Offset = self.powerTablePosition + self.voltageTable3Offset

            self.data['Voltage table 3'].append({
                'name': 'table offset',
                'value': str(hex(self.fullvoltageTable3Offset)),
                'unit': '',
                'position': str(hex(self.powerTablePosition + self.voltageTable3Offset)),
                'length' :  ''
            })

            for voltage_counter in range(self.voltageTable3count):
                pos_voltage = self.fullvoltageTable3Offset + voltage_counter * 8
                self.data['Voltage table 3'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 1',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })
                pos_voltage += 2
                self.data['Voltage table 3'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 2',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })
                pos_voltage += 2
                self.data['Voltage table 3'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 3',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })
                pos_voltage += 2
                self.data['Voltage table 3'].append({
                    'name': 'DPM ' + str(voltage_counter) + '- value 4',
                    'value': str(BytesReader.read_int16(self.rom, pos_voltage)),
                    'unit': 'mV',
                    'position': str(hex(pos_voltage)),
                    'length' : '16 bits'
                })

    def parse_mem_freq(self):
        if self.powerTablePosition:
            self.pos_memoryFrequencyTableCount = self.powerTablePosition + self.memoryFrequencyTableCountOffset
            self.memoryFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_memoryFrequencyTableCount)
            self.data['MEM freq table'].append({
                'name': 'MEM freq table count',
                'value': str(self.memoryFrequencyTableCount),
                'unit': '',
                'position': str(hex(self.pos_memoryFrequencyTableCount)),
                'length' : '8 bits'
            })

            for mem_freq_counter in range(self.memoryFrequencyTableCount):
                pos_mem_freq = self.powerTablePosition + self.memoryFrequencyTableOffset +  mem_freq_counter * 13
                self.data['MEM freq table'].append({
                    'name': 'DPM ' + str(mem_freq_counter) + ' : frequency',
                    'value': str(BytesReader.read_int24(self.rom, pos_mem_freq)),
                    'unit': '10 KHz',
                    'position': str(hex(pos_mem_freq)),
                    'length' : '24 bits'
                })

    def parse_gpu_mem(self):
        if self.powerTablePosition:
            self.pos_gpuFrequencyTableCount = self.powerTablePosition + self.gpuFrequencyTableCountOffset
            self.gpuFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_gpuFrequencyTableCount)
            self.data['GPU freq table'].append({
                'name': 'GPU freq table count',
                'value': str(self.gpuFrequencyTableCount),
                'unit': '',
                'position': str(hex(self.pos_gpuFrequencyTableCount)),
                'length' : '8 bits'
            })

            for gpu_freq_counter in range(self.gpuFrequencyTableCount):
                pos_gpu_freq = self.powerTablePosition + self.gpuFrequencyTableOffset + gpu_freq_counter * 11
                pos_gpu_volt = pos_gpu_freq + 3
                self.data['GPU freq table'].append({
                    'name': 'DPM ' + str(gpu_freq_counter) + ' : frequency',
                    'value': str(BytesReader.read_int24(self.rom, pos_gpu_freq)),
                    'unit': '10 KHz',
                    'position': str(hex(pos_gpu_freq)),
                    'length' : '24 bits'
                })

    def parse_fantable(self):
        if self.fanTablePosition > 0:
            pos_value = self.fanTablePosition + 1
            self.data['Fan table'].append({
                'name': 'Temp hysteresis',
                'value': str(BytesReader.read_int8(self.rom, pos_value)),
                'unit': '°C',
                'position': str(hex(pos_value)),
                'length' : '8 bits'
            })
            for temp_counter in range(3):
                pos_value = self.fanTablePosition + 2 + temp_counter * 2
                self.data['Fan table'].append({
                    'name': 'Fan temp ' + str(temp_counter + 1),
                    'value': str(BytesReader.read_int16(self.rom, pos_value)),
                    'unit': '100 °C',
                    'position': str(hex(pos_value)),
                    'length' : '16 bits'
                })
            for speed_counter in range(3):
                pos_value = self.fanTablePosition + 8 + speed_counter * 2
                self.data['Fan table'].append({
                    'name': 'Fan speed ' + str(speed_counter + 1),
                    'value': str(BytesReader.read_int16(self.rom, pos_value)),
                    'unit': '100 %',
                    'position': str(hex(pos_value)),
                    'length' : '16 bits'
                })
            pos_value = self.fanTablePosition + 14
            self.data['Fan table'].append({
                'name': 'Max temp',
                'value': str(BytesReader.read_int16(self.rom, pos_value)),
                'unit': '100 °C',
                'position': str(hex(pos_value)),
                'length' : '16 bits'
            })
            pos_value = self.fanTablePosition + 16
            self.data['Fan table'].append({
                'name': 'Fan control type',
                'value': str(BytesReader.read_int8(self.rom, pos_value)),
                'unit': '',
                'position': str(hex(pos_value)),
                'length' : '8 bits'
            })
            pos_value = self.fanTablePosition + 17
            self.data['Fan table'].append({
                'name': 'PWM fan max',
                'value': str(BytesReader.read_int8(self.rom, pos_value)),
                'unit': '°C',
                'position': str(hex(pos_value)),
                'length' : '8 bits'
            })

    def parse_all(self):

        print('parsing rom ...')

        self.parse_positions()

        self.parse_overview()

        self.parse_powertable()

        self.parse_voltagetable()

        self.parse_mem_freq()

        self.parse_gpu_mem()

        self.parse_fantable()

    def is_supported(self):
        return True  # TODO add device id check
