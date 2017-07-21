# -*- coding: utf-8 -*-

from pprint import pprint
from tools import BytesReader, BytesWriter

supportedDevIDs = {
    '0x6658',
    '0x665c',
    '0x665d',
    '0x665f',
    '0x67a0',
    '0x67a1',
    '0x67a2',
    '0x67a8',
    '0x67a9',
    '0x67aa',
    '0x67b0',
    '0x67b1',
    '0x67b9',
}

vrm_types = {
    '0x22': 'fsw 1 VDDC',
    '0x23': 'fsw 2 VDDI',
    '0x26': 'hidden VDDC/VDDCI',
    '0x33': 'Voltage Protection',
    '0x34': 'Current Protection',
    '0x38': 'LLC',
    '0x3d': 'VDDCR Limit',
    '0x8d': 'VDDC Offset',
    '0x8e': 'VDDCI Offset'
}

vrm_unit = {
    '0x22': 'Hz',
    '0x23': 'Hz',
    '0x26': '',
    '0x33': '',
    '0x34': 'A',
    '0x38': '',
    '0x3d': 'mV',
    '0x8d': 'mV',
    '0x8e': 'mV'
}


class HawaiiBios:


    def __init__(self, rom: bytes):
        self.rom = rom
        self.data = {
            'Overview': [],
            'Powerplay': [],
            'VDDCI states': [],
            'GPU freq table': [],
            'MEM freq table': [],
            'Start VCE limit table': [],
            'Start ACP limit table': [],
            'Start SAMU limit table': [],
            'Start UVD limit table': [],
            'Fan Profile': [],
            'VRM settings': []
        }
        self.parse_all()

    def calculate_checksum(self):
        oldchecksum = BytesReader.read_int8(self.rom, 33)
        size = BytesReader.read_int8(self.rom, 2) * 512

        newchecksum = oldchecksum - sum(BytesReader.read_int8(self.rom, i) for i in range(size))

        if oldchecksum == newchecksum:
            print('checksum ok')
        else:
            print('wrong checksum')

        self.rom = BytesWriter.write_int8(self.rom, 33, newchecksum % 256)
        print('checksum saved')


    def parse_positions(self):

        self.pos_pciInfoPosition = 24
        self.pciInfoPosition = BytesReader.read_int16(self.rom, self.pos_pciInfoPosition)
        print('pciInfoPosition :', hex(self.pciInfoPosition))

        self.pos_headerPosition = 72
        self.headerPosition = BytesReader.read_int16(self.rom, self.pos_headerPosition)
        print('headerPosition :', hex(self.headerPosition))

        self.pos_dataPointersPosition = 32 + self.headerPosition
        self.dataPointersPosition = BytesReader.read_int16(self.rom, self.pos_dataPointersPosition)
        print('dataPointersPosition :', hex(self.dataPointersPosition))

        self.pos_powerTablePosition = 34 + self.dataPointersPosition
        self.powerTablePosition = BytesReader.read_int16(self.rom, self.pos_powerTablePosition)
        print('powerTablePosition :', hex(self.powerTablePosition))

        self.pos_gpuVRMTablePosition = 68 + self.dataPointersPosition
        self.gpuVRMTablePosition = BytesReader.read_int16(self.rom, self.pos_gpuVRMTablePosition)
        print('gpuVRMTablePosition :', hex(self.gpuVRMTablePosition))

        self.powerTableSize = BytesReader.read_int16(self.rom, self.powerTablePosition)
        print('powerTableSize :', self.powerTableSize)

        self.pos_clockInfoOffset = 11 + self.powerTablePosition
        self.clockInfoOffset = BytesReader.read_int16(self.rom, self.pos_clockInfoOffset)
        print('clockInfoOffset :', hex(self.clockInfoOffset))

        self.pos_fanTablePosition = 42 + self.powerTablePosition
        self.fanTablePosition = self.powerTablePosition + BytesReader.read_int16(self.rom, self.pos_fanTablePosition)
        print('fanTablePosition :', hex(self.fanTablePosition))

        self.pos_gpuFrequencyTableOffset = 54 + self.powerTablePosition
        self.gpuFrequencyTableOffset = BytesReader.read_int16(self.rom, self.pos_gpuFrequencyTableOffset)
        print('gpuFrequencyTableOffset :', hex(self.gpuFrequencyTableOffset))

        # TEMP (Only gets first VDDCI) - +4 to skip number of vddci states(1 byte) and first frequency(3 bytes)
        self.pos_AUXvoltageOffset = 56 + self.powerTablePosition
        self.AUXvoltageOffset = BytesReader.read_int16(self.rom, self.pos_AUXvoltageOffset)
        print('AUXvoltageOffset :', hex(self.AUXvoltageOffset))

        self.pos_memoryFrequencyTableOffset = 58 + self.powerTablePosition
        self.memoryFrequencyTableOffset = BytesReader.read_int16(self.rom, self.pos_memoryFrequencyTableOffset)
        print('memoryFrequencyTableOffset :', hex(self.memoryFrequencyTableOffset))

        self.pos_limitsPointersOffset = 44 + self.powerTablePosition
        self.limitsPointersOffset = BytesReader.read_int16(self.rom, self.pos_limitsPointersOffset)
        print('limitsPointersOffset :', hex(self.limitsPointersOffset))

        self.pos_VCETableOffset = 10 + self.limitsPointersOffset + self.powerTablePosition
        self.VCETableOffset = BytesReader.read_int16(self.rom, self.pos_VCETableOffset)
        print('VCETableOffset :', hex(self.VCETableOffset))

        self.pos_VCEunknownStatesNum = 1 + self.VCETableOffset + self.powerTablePosition
        self.VCEunknownStatesNum = BytesReader.read_int8(self.rom, self.pos_VCEunknownStatesNum)
        print('VCEunknownStatesNum :', hex(self.VCEunknownStatesNum))

        self.VCELimitTableOffset = self.VCETableOffset + 2 + self.VCEunknownStatesNum * 6
        print('VCELimitTableOffset :', hex(self.VCELimitTableOffset))

        self.pos_UVDTableOffset = 12 + self.powerTablePosition + self.limitsPointersOffset
        self.UVDTableOffset = BytesReader.read_int16(self.rom, self.pos_UVDTableOffset)
        print('UVDTableOffset :', hex(self.UVDTableOffset))

        self.pos_UVDunknownStatesNum = 1 + self.powerTablePosition + self.UVDTableOffset
        self.UVDunknownStatesNum = BytesReader.read_int8(self.rom, self.pos_UVDunknownStatesNum)
        print('UVDunknownStatesNum :', hex(self.UVDunknownStatesNum))

        self.UVDLimitTableOffset = self.UVDTableOffset + 2 + self.UVDunknownStatesNum * 6
        print('UVDLimitTableOffset :', hex(self.UVDLimitTableOffset))

        self.pos_SAMULimitTableOffset = 14 + self.powerTablePosition + self.limitsPointersOffset
        self.SAMULimitTableOffset = BytesReader.read_int16(self.rom, self.pos_SAMULimitTableOffset)
        print('SAMULimitTableOffset :', hex(self.SAMULimitTableOffset))

        self.pos_ACPLimitTableOffset = 18 + self.powerTablePosition + self.limitsPointersOffset
        self.ACPLimitTableOffset = BytesReader.read_int16(self.rom, self.pos_ACPLimitTableOffset)
        print('ACPLimitTableOffset :', hex(self.ACPLimitTableOffset))

        self.pos_tdpLimitOffset = 20 + self.powerTablePosition + self.limitsPointersOffset
        self.tdpLimitOffset = 3 + BytesReader.read_int16(self.rom, self.pos_tdpLimitOffset)
        print('tdpLimitOffset :', hex(self.tdpLimitOffset))

        self.powerDeliveryLimitOffset = self.tdpLimitOffset + 12
        print('powerDeliveryLimitOffset :', hex(self.powerDeliveryLimitOffset))

        self.tdcLimitOffset = self.tdpLimitOffset + 2
        print('tdcLimitOffset :', hex(self.tdcLimitOffset))

        self.pos_CCCLimitsPosition = 44 + self.powerTablePosition
        self.CCCLimitsPosition = self.powerTablePosition + BytesReader.read_int16(self.rom, self.pos_CCCLimitsPosition)
        print('CCCLimitsPosition :', hex(self.CCCLimitsPosition))


    def parse_overview(self):

        self.pos_biosName = 220
        self.data['Overview'].append({
            'name': 'bios name',
            'value': BytesReader.read_str(self.rom, self.pos_biosName, 32),
            'unit': '',
            'position': str(hex(self.pos_biosName)),
            'length' : '32 char'
        })

        self.pos_devIDstr = 6 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'dev id',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_devIDstr))),
            'unit': '' ,
            'position': str(hex(self.pos_devIDstr)),
            'length' : '16 bits'
        })

        self.pos_vendorID = 4 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'vendor id',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_vendorID))),
            'unit': '',
            'position': str(hex(self.pos_vendorID)),
            'length' : '16 bits'
        })

        self.pos_productData = 8 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'product data',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_productData))),
            'unit': '',
            'position': str(hex(self.pos_productData)),
            'length' : '16 bits'
        })

        self.pos_structureLength = 10 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'structure length',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_structureLength))),
            'unit': '',
            'position': str(hex(self.pos_structureLength)),
            'length' : '16 bits'
        })

        self.pos_structureRevision = 12 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'structure revision',
            'value': str(hex(BytesReader.read_int8(self.rom, self.pos_structureRevision))),
            'unit': '',
            'position': str(hex(self.pos_structureRevision)),
            'length' : '8 bits'
        })

        self.pos1_classCode = 13 + self.pciInfoPosition
        self.pos2_classCode = 14 + self.pciInfoPosition
        self.pos3_classCode = 15 + self.pciInfoPosition
        class_code = hex(BytesReader.read_int8(self.rom, self.pos1_classCode)) \
                     + ' - ' \
                     + hex(BytesReader.read_int8(self.rom, self.pos2_classCode)) \
                     + ' - ' \
                     + hex(BytesReader.read_int8(self.rom, self.pos3_classCode))
        self.data['Overview'].append({
            'name': 'structure revision',
            'value': class_code,
            'unit': '',
            'position': class_code,
            'length' : ''
        })

        self.pos_imageLength = 16 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'image length',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_imageLength))),
            'unit': '',
            'position': str(hex(self.pos_imageLength)),
            'length' : '16 bits'
        })

        self.pos_revisionLevel = 18 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'revision level',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_revisionLevel))),
            'unit': '',
            'position': str(hex(self.pos_revisionLevel)),
            'length' : '16 bits'
        })

        self.pos_codeType = 20 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'code type',
            'value': str(hex(BytesReader.read_int8(self.rom, self.pos_codeType))),
            'unit': '',
            'position': str(hex(self.pos_codeType)),
            'length' : '8 bits'
        })

        self.pos_indicator = 21 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'indicator',
            'value': str(hex(BytesReader.read_int8(self.rom, self.pos_indicator))),
            'unit': '',
            'position': str(hex(self.pos_indicator)),
            'length' : '8 bits'
        })

        self.pos_reserved = 22 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'reserved',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_reserved))),
            'unit': '',
            'position': str(hex(self.pos_reserved)),
            'length' : '16 bits'
        })

        self.pos_SSVID = self.pciInfoPosition - 12
        self.data['Overview'].append({
            'name': 'SSVID',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_SSVID))[2:]),
            'unit': '',
            'position': str(hex(self.pos_SSVID)),
            'length' : '16 bits'
        })

        self.pos_SSDID = self.pciInfoPosition - 14
        self.data['Overview'].append({
            'name': 'SSDID',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_SSDID))[2:]),
            'unit': '',
            'position': str(hex(self.pos_SSDID)),
            'length' : '16 bits'
        })


        self.pos_gpuMaxClock = self.CCCLimitsPosition + 2
        self.data['Overview'].append({
            'name': 'gpu max clock',
            'value': str(BytesReader.read_int24(self.rom, self.pos_gpuMaxClock)),
            'unit': '10 KHz',
            'position': str(hex(self.pos_gpuMaxClock)),
            'length' : '24 bits'
        })

        self.pos_memMaxClock = self.CCCLimitsPosition + 6
        self.data['Overview'].append({
            'name': 'mem max clock',
            'value': str(BytesReader.read_int24(self.rom, self.pos_memMaxClock)),
            'unit': '10 KHz',
            'position': str(hex(self.pos_memMaxClock)),
            'length' : '24 bits'
        })


    def parse_powerplay(self):

        temp_pos = self.powerTablePosition + self.clockInfoOffset

        self.data['Powerplay'].append({
            'name': 'GPU clock 1',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 2)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 2)),
            'length' : '24 bits'
        })
        self.data['Powerplay'].append({
            'name': 'GPU clock 2',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 11)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 11)),
            'length' : '24 bits'
        })
        self.data['Powerplay'].append({
            'name': 'GPU clock 3',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 20)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 20)),
            'length' : '24 bits'
        })
        self.data['Powerplay'].append({
            'name': 'Mem clock 1',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 5)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 5)),
            'length' : '24 bits'
        })
        self.data['Powerplay'].append({
            'name': 'Mem clock 2',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 14)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 14)),
            'length' : '24 bits'
        })
        self.data['Powerplay'].append({
            'name': 'Mem clock 3',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 23)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 23)),
            'length' : '24 bits'
        })
        self.data['Powerplay'].append({
            'name': 'TDP max',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.tdpLimitOffset)),
            'unit': 'W',
            'position': str(hex(self.powerTablePosition + self.tdpLimitOffset)),
            'length' : '16 bits'
        })
        self.data['Powerplay'].append({
            'name': 'Power limit',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset)),
            'unit': 'W',
            'position': str(hex(self.powerTablePosition + self.powerDeliveryLimitOffset)),
            'length' : '16 bits'
        })
        self.data['Powerplay'].append({
            'name': 'TDC limit',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.tdcLimitOffset)),
            'unit': 'A',
            'position': str(hex(self.powerTablePosition + self.tdcLimitOffset)),
            'length' : '16 bits'
        })
        self.data['Powerplay'].append({
            'name': 'Max ASIC temp',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset + 2)),
            'unit': '°C',
            'position': str(hex(self.powerTablePosition + self.powerDeliveryLimitOffset + 2)),
            'length' : '16 bits'
        })


    def parse_vddci(self):

        self.pos_vddciTableCount = self.powerTablePosition + self.AUXvoltageOffset
        self.vddciTableCount = BytesReader.read_int8(self.rom, self.pos_vddciTableCount)
        self.data['VDDCI states'].append({
            'name': 'VDDCI table count',
            'value': str(BytesReader.read_int8(self.rom, self.pos_vddciTableCount)),
            'unit': '',
            'position': str(hex(self.pos_vddciTableCount)),
            'length' : '8 bits'
        })

        for vddcicounter in range(self.vddciTableCount):
            pos_vddci_freq = self.powerTablePosition + self.AUXvoltageOffset + 1 + (vddcicounter * 5)
            pos_vddci_volt = pos_vddci_freq + 3
            self.data['VDDCI states'].append({
                'name': 'DPM ' + str(vddcicounter) + ' : frequency',
                'value': str(BytesReader.read_int24(self.rom, pos_vddci_freq)),
                'unit': '10 KHz',
                'position': str(hex(pos_vddci_freq)),
                'length' : '24 bits'
            })
            self.data['VDDCI states'].append({
                'name': 'DPM ' + str(vddcicounter) + ' : voltage',
                'value': str(BytesReader.read_int16(self.rom, pos_vddci_volt)),
                'unit': 'mV',
                'position': str(hex(pos_vddci_volt)),
                'length' : '16 bits'
            })


    def parse_mem_freq(self):

        self.pos_memoryFrequencyTableCount = self.powerTablePosition + self.memoryFrequencyTableOffset
        self.memoryFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_memoryFrequencyTableCount)
        self.data['MEM freq table'].append({
            'name': 'MEM freq table count',
            'value': str(self.memoryFrequencyTableCount),
            'unit': '',
            'position': str(hex(self.pos_memoryFrequencyTableCount)),
            'length' : '8 bits'
        })

        for mem_freq_counter in range(self.memoryFrequencyTableCount):
            pos_mem_freq = self.powerTablePosition + self.memoryFrequencyTableOffset + 1 + (mem_freq_counter * 5)
            pos_mem_volt = pos_mem_freq + 3
            self.data['MEM freq table'].append({
                'name': 'DPM ' + str(mem_freq_counter) + ' : frequency',
                'value': str(BytesReader.read_int24(self.rom, pos_mem_freq)),
                'unit': '10 KHz',
                'position': str(hex(pos_mem_freq)),
                'length' : '24 bits'
            })
            self.data['MEM freq table'].append({
                'name': 'DPM ' + str(mem_freq_counter) + ' : voltage',
                'value': str(BytesReader.read_int16(self.rom, pos_mem_volt)),
                'unit': '10 KHz',
                'position': str(hex(pos_mem_volt)),
                'length' : '16 bits'
            })


    def parse_gpu_mem(self):

        self.pos_gpuFrequencyTableCount = self.powerTablePosition + self.gpuFrequencyTableOffset
        self.gpuFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_gpuFrequencyTableCount)
        self.data['GPU freq table'].append({
            'name': 'GPU freq table count',
            'value': str(self.gpuFrequencyTableCount),
            'unit': '',
            'position': str(hex(self.pos_gpuFrequencyTableCount)),
            'length' : '8 bits'
        })

        self.GPUFreqTable = []
        for gpu_freq_counter in range(self.gpuFrequencyTableCount):
            pos_gpu_freq = self.powerTablePosition + self.gpuFrequencyTableOffset + 1 + (gpu_freq_counter * 5)
            pos_gpu_volt = pos_gpu_freq + 3
            self.data['GPU freq table'].append({
                'name': 'DPM ' + str(gpu_freq_counter) + ' : frequency',
                'value': str(BytesReader.read_int24(self.rom, pos_gpu_freq)),
                'unit': '10 KHz',
                'position': str(hex(pos_gpu_freq)),
                'length' : '24 bits'
            })
            self.data['GPU freq table'].append({
                'name': 'DPM ' + str(gpu_freq_counter) + ' : voltage',
                'value': str(BytesReader.read_int16(self.rom, pos_gpu_volt)),
                'unit': '10 KHz',
                'position': str(hex(pos_gpu_volt)),
                'length' : '16 bits'
            })


    def parse_vce_limit(self):

        self.pos_StartVCELimitTable = self.powerTablePosition + self.VCELimitTableOffset
        self.StartVCELimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartVCELimitTable)
        self.data['Start VCE limit table'].append({
            'name': 'Start VCE limit table count',
            'value': str(self.StartVCELimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartVCELimitTable)),
            'length' : '8 bits'
        })

        for vce in range(self.StartVCELimitTable_count):
            pos_vce = self.powerTablePosition + self.VCELimitTableOffset + 1 + (vce * 3)
            self.data['Start VCE limit table'].append({
                'name': 'DPM ' + str(vce) + ' : ' + str(BytesReader.read_int8(self.rom, pos_vce + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_vce)),
                'unit': 'mV',
                'position': str(hex(pos_vce)),
                'length' : '16 bits'
            })


    def parse_uvd_limit(self):

        self.pos_StartUVDLimitTable = self.powerTablePosition + self.UVDLimitTableOffset
        self.StartUVDLimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartUVDLimitTable)
        self.data['Start UVD limit table'].append({
            'name': 'Start UVD limit table count',
            'value': str(self.StartUVDLimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartUVDLimitTable)),
            'length' : '8 bits'
        })

        for uvd in range(self.StartUVDLimitTable_count):
            pos_uvd = self.powerTablePosition + self.UVDLimitTableOffset + 1 + (uvd * 3)
            self.data['Start UVD limit table'].append({
                'name': 'DPM ' + str(uvd) + ' : ' + str(BytesReader.read_int8(self.rom, pos_uvd + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_uvd)),
                'unit': 'mV',
                'position': str(hex(pos_uvd)),
                'length' : '16 bits'
            })


    def parse_samu_limit(self):

        self.pos_StartSAMULimitTable = self.powerTablePosition + self.SAMULimitTableOffset + 1
        self.StartSAMULimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartSAMULimitTable)
        self.data['Start SAMU limit table'].append({
            'name': 'Start SAMU limit table count',
            'value': str(self.StartSAMULimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartSAMULimitTable)),
            'length' : '8 bits'
        })

        for samu in range(self.StartSAMULimitTable_count):
            pos_samu = self.powerTablePosition + self.SAMULimitTableOffset + 2 + (samu * 5)
            self.data['Start SAMU limit table'].append({
                'name': 'DPM ' + str(samu) + ' : ' + str(BytesReader.read_int24(self.rom, pos_samu + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_samu)),
                'unit': 'mV',
                'position': str(hex(pos_samu)),
                'length' : '16 bits'
            })


    def parse_acp_limit(self):

        self.pos_StartACPLimitTable = self.powerTablePosition + self.ACPLimitTableOffset + 1
        self.StartACPLimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartACPLimitTable)
        self.data['Start ACP limit table'].append({
            'name': 'Start ACP limit table count',
            'value': str(self.StartACPLimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartACPLimitTable)),
            'length' : '8 bits'
        })

        for acp in range(self.StartACPLimitTable_count):
            pos_acp = self.powerTablePosition + self.ACPLimitTableOffset + 2 + (acp * 5)
            self.data['Start ACP limit table'].append({
                'name': 'DPM ' + str(acp) + ' : ' + str(BytesReader.read_int24(self.rom, pos_acp + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_acp)),
                'unit': 'mV',
                'position': str(hex(pos_acp)),
                'length' : '16 bits'
            })


    def parse_fan_profile(self):

        self.data['Fan Profile'].append({
            'name': 'Temp hysteresis',
            'value': str(BytesReader.read_int8(self.rom, self.fanTablePosition + 1)),
            'unit': '°C',
            'position': str(hex(self.fanTablePosition + 1)),
            'length' : '8 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Temp target 1',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 2)),
            'unit': '100 °C',
            'position': str(hex(self.fanTablePosition + 2)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Temp target 2',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 4)),
            'unit': '100 °C',
            'position': str(hex(self.fanTablePosition + 4)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Temp target 3',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 6)),
            'unit': '100 °C',
            'position': str(hex(self.fanTablePosition + 6)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Fan speed 1',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 8)),
            'unit': '100 %',
            'position': str(hex(self.fanTablePosition + 8)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Fan speed 2',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 10)),
            'unit': '100 %',
            'position': str(hex(self.fanTablePosition + 10)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Fan speed 3',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 12)),
            'unit': '100 %',
            'position': str(hex(self.fanTablePosition + 12)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Max temp',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 14)),
            'unit': '100 °C',
            'position': str(hex(self.fanTablePosition + 14)),
            'length' : '16 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'Fan control type',
            'value': str(BytesReader.read_int8(self.rom, self.fanTablePosition + 16)),
            'unit': '°C',
            'position': str(hex(self.fanTablePosition + 16)),
            'length' : '8 bits'
        })

        self.data['Fan Profile'].append({
            'name': 'PWM fan max',
            'value': str(BytesReader.read_int8(self.rom, self.fanTablePosition + 17)),
            'unit': '%',
            'position': str(hex(self.fanTablePosition + 17)),
            'length' : '8 bits'
        })


    def parse_vrm_setting(self):

        self.pos_vrmList_size = self.gpuVRMTablePosition + 6
        self.vrmList_size = BytesReader.read_int16(self.rom, self.pos_vrmList_size)
        self.data['VRM settings'].append({
            'name': 'VRM table count',
            'value': str(self.vrmList_size),
            'unit': '',
            'position': str(hex(self.pos_vrmList_size)),
            'length' : '16 bits'
        })

        for vrm in range(2, self.vrmList_size, 2):
            pos_temp = self.gpuVRMTablePosition + 6 + vrm
            temp = BytesReader.read_int16(self.rom, pos_temp)
            if hex(temp) in vrm_types:
                value = BytesReader.read_int16(self.rom, self.gpuVRMTablePosition + 8 + vrm)
                self.data['VRM settings'].append({
                    'name': vrm_types[hex(temp)],
                    'value': str(value),
                    'unit': vrm_unit[hex(temp)],
                    'position': str(hex(pos_temp)),
                    'length' : '16 bits'
                })
            else:
                print('unknow VRM :', hex(temp), '@', hex(pos_temp))


    def parse_all(self):

        print('parsing rom ...')

        self.parse_positions()

        self.parse_overview()

        self.parse_powerplay()

        self.parse_vddci()

        self.parse_mem_freq()

        self.parse_gpu_mem()

        self.parse_vce_limit()

        self.parse_uvd_limit()

        self.parse_samu_limit()

        self.parse_acp_limit()

        self.parse_fan_profile()

        self.parse_vrm_setting()


    def is_supported(self):
        return any(f['name'] == 'dev id' and f['value'] in supportedDevIDs for f in self.data['Overview'])
