# -*- coding: utf-8 -*-

from pprint import pprint
from tools import BytesReader

supportedDevIDs = {
    '0x67a0',
    '0x67a1',
    '0x67a2',
    '0x67a8',
    '0x67a9',
    '0x67aa',
    '0x67b0',
    '0x67b1',
    '0x67b9'
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
        self.parse()

    def parse(self):

        print('parsing rom ...')

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

        # Overview

        self.pos_biosName = 220
        self.data['Overview'].append({
            'name': 'bios name',
            'value': BytesReader.read_str(self.rom, self.pos_biosName, 32),
            'unit': '',
            'position': str(hex(self.pos_biosName))
        })

        self.pos_devIDstr = 6 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'dev id',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_devIDstr))),
            'unit': '' ,
            'position': str(hex(self.pos_devIDstr))
        })

        if self.data['Overview'][-1]['value'] in supportedDevIDs:
            print('>> Ok this rom device is supported')
        else:
            print('>> Warning this rom device seems not supported')

        self.pos_vendorID = 4 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'vendor id',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_vendorID))),
            'unit': '',
            'position': str(hex(self.pos_vendorID))
        })

        self.pos_productData = 8 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'product data',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_productData))),
            'unit': '',
            'position': str(hex(self.pos_productData))
        })

        self.pos_structureLength = 10 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'structure length',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_structureLength))),
            'unit': '',
            'position': str(hex(self.pos_structureLength))
        })

        self.pos_structureRevision = 12 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'structure revision',
            'value': str(hex(BytesReader.read_int8(self.rom, self.pos_structureRevision))),
            'unit': '',
            'position': str(hex(self.pos_structureRevision))
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
            'position': class_code
        })

        self.pos_imageLength = 16 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'image length',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_imageLength))),
            'unit': '',
            'position': str(hex(self.pos_imageLength))
        })

        self.pos_revisionLevel = 18 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'revision level',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_revisionLevel))),
            'unit': '',
            'position': str(hex(self.pos_revisionLevel))
        })

        self.pos_codeType = 20 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'code type',
            'value': str(hex(BytesReader.read_int8(self.rom, self.pos_codeType))),
            'unit': '',
            'position': str(hex(self.pos_codeType))
        })

        self.pos_indicator = 21 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'indicator',
            'value': str(hex(BytesReader.read_int8(self.rom, self.pos_indicator))),
            'unit': '',
            'position': str(hex(self.pos_indicator))
        })

        self.pos_reserved = 22 + self.pciInfoPosition
        self.data['Overview'].append({
            'name': 'reserved',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_reserved))),
            'unit': '',
            'position': str(hex(self.pos_reserved))
        })

        self.pos_SSVID = self.pciInfoPosition - 12
        self.data['Overview'].append({
            'name': 'SSVID',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_SSVID))[2:]),
            'unit': '',
            'position': str(hex(self.pos_SSVID))
        })

        self.pos_SSDID = self.pciInfoPosition - 14
        self.data['Overview'].append({
            'name': 'SSDID',
            'value': str(hex(BytesReader.read_int16(self.rom, self.pos_SSDID))[2:]),
            'unit': '',
            'position': str(hex(self.pos_SSDID))
        })


        self.pos_gpuMaxClock = self.CCCLimitsPosition + 2
        self.data['Overview'].append({
            'name': 'gpu max clock',
            'value': str(BytesReader.read_int24(self.rom, self.pos_gpuMaxClock)),
            'unit': '10 KHz',
            'position': str(hex(self.pos_gpuMaxClock))
        })

        self.pos_memMaxClock = self.CCCLimitsPosition + 6
        self.data['Overview'].append({
            'name': 'mem max clock',
            'value': str(BytesReader.read_int24(self.rom, self.pos_memMaxClock)),
            'unit': '10 KHz',
            'position': str(hex(self.pos_memMaxClock))
        })

        # Powerplay

        temp_pos = self.powerTablePosition + self.clockInfoOffset

        self.data['Powerplay'].append({
            'name': 'GPU clock 1',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 2)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 2))
        })
        self.data['Powerplay'].append({
            'name': 'GPU clock 2',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 11)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 11))
        })
        self.data['Powerplay'].append({
            'name': 'GPU clock 3',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 20)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 20))
        })
        self.data['Powerplay'].append({
            'name': 'Mem clock 1',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 5)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 5))
        })
        self.data['Powerplay'].append({
            'name': 'Mem clock 2',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 14)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 14))
        })
        self.data['Powerplay'].append({
            'name': 'Mem clock 3',
            'value': str(BytesReader.read_int24(self.rom, temp_pos + 23)),
            'unit': '10 KHz',
            'position': str(hex(temp_pos + 23))
        })
        self.data['Powerplay'].append({
            'name': 'TDP max',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.tdpLimitOffset)),
            'unit': 'W',
            'position': str(hex(self.powerTablePosition + self.tdpLimitOffset))
        })
        self.data['Powerplay'].append({
            'name': 'Power limit',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset)),
            'unit': 'W',
            'position': str(hex(self.powerTablePosition + self.powerDeliveryLimitOffset))
        })
        self.data['Powerplay'].append({
            'name': 'TDC limit',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.tdcLimitOffset)),
            'unit': 'A',
            'position': str(hex(self.powerTablePosition + self.tdcLimitOffset))
        })
        self.data['Powerplay'].append({
            'name': 'Max ASIC temp',
            'value': str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset + 2)),
            'unit': '°C',
            'position': str(hex(self.powerTablePosition + self.powerDeliveryLimitOffset + 2))
        })

        # VDDCI states

        self.pos_vddciTableCount = self.powerTablePosition + self.AUXvoltageOffset
        self.vddciTableCount = BytesReader.read_int8(self.rom, self.pos_vddciTableCount)
        self.data['VDDCI states'].append({
            'name': 'VDDCI table count',
            'value': str(BytesReader.read_int8(self.rom, self.pos_vddciTableCount)),
            'unit': '',
            'position': str(hex(self.pos_vddciTableCount))
        })

        for vddcicounter in range(self.vddciTableCount):
            pos_vddci = self.powerTablePosition + self.AUXvoltageOffset + 1 + (vddcicounter * 5)
            self.data['VDDCI states'].append({
                'name': 'DPM ' + str(vddcicounter),
                'value': str(BytesReader.read_int24(self.rom, pos_vddci)),
                'unit': '10 KHz',
                'position': str(hex(pos_vddci))
            })

        # MEM freq table

        self.pos_memoryFrequencyTableCount = self.powerTablePosition + self.memoryFrequencyTableOffset
        self.memoryFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_memoryFrequencyTableCount)
        self.data['MEM freq table'].append({
            'name': 'MEM freq table count',
            'value': str(self.memoryFrequencyTableCount),
            'unit': '',
            'position': str(hex(self.pos_memoryFrequencyTableCount))
        })

        for mem_freq_counter in range(self.memoryFrequencyTableCount):
            pos_mem_freq = self.powerTablePosition + self.memoryFrequencyTableOffset + 1 + (mem_freq_counter * 5)
            self.data['MEM freq table'].append({
                'name': 'DPM ' + str(mem_freq_counter),
                'value': str(BytesReader.read_int24(self.rom, pos_mem_freq)),
                'unit': '10 KHz',
                'position': str(hex(pos_mem_freq))
            })

        # GPU freq table

        self.pos_gpuFrequencyTableCount = self.powerTablePosition + self.gpuFrequencyTableOffset
        self.gpuFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_gpuFrequencyTableCount)
        self.data['GPU freq table'].append({
            'name': 'GPU freq table count',
            'value': str(self.gpuFrequencyTableCount),
            'unit': '',
            'position': str(hex(self.pos_gpuFrequencyTableCount))
        })

        self.GPUFreqTable = []
        for gpu_freq_counter in range(self.gpuFrequencyTableCount):
            pos_gpu_freq = self.powerTablePosition + self.gpuFrequencyTableOffset + 1 + (gpu_freq_counter * 5)
            self.data['GPU freq table'].append({
                'name': 'DPM ' + str(gpu_freq_counter),
                'value': str(BytesReader.read_int24(self.rom, pos_gpu_freq)),
                'unit': '10 KHz',
                'position': str(hex(pos_gpu_freq))
            })

        # Start VCE limit tables

        self.pos_StartVCELimitTable = self.powerTablePosition + self.VCELimitTableOffset
        self.StartVCELimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartVCELimitTable)
        self.data['Start VCE limit table'].append({
            'name': 'Start VCE limit table count',
            'value': str(self.StartVCELimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartVCELimitTable))
        })

        for vce in range(self.StartVCELimitTable_count):
            pos_vce = self.powerTablePosition + self.VCELimitTableOffset + 1 + (vce * 3)
            self.data['Start VCE limit table'].append({
                'name': 'DPM ' + str(BytesReader.read_int8(self.rom, pos_vce + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_vce)),
                'unit': 'mV',
                'position': str(hex(pos_vce))
            })

        # Start UVD limit tables

        self.pos_StartUVDLimitTable = self.powerTablePosition + self.UVDLimitTableOffset
        self.StartUVDLimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartUVDLimitTable)
        self.data['Start UVD limit table'].append({
            'name': 'Start UVD limit table count',
            'value': str(self.StartUVDLimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartUVDLimitTable))
        })

        for uvd in range(self.StartUVDLimitTable_count):
            pos_uvd = self.powerTablePosition + self.UVDLimitTableOffset + 1 + (uvd * 3)
            self.data['Start UVD limit table'].append({
                'name': 'DPM ' + str(BytesReader.read_int8(self.rom, pos_uvd + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_uvd)),
                'unit': 'mV',
                'position': str(hex(pos_uvd))
            })

        # Start SAMU limit tables

        self.pos_StartSAMULimitTable = self.powerTablePosition + self.SAMULimitTableOffset + 1
        self.StartSAMULimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartSAMULimitTable)
        self.data['Start SAMU limit table'].append({
            'name': 'Start SAMU limit table count',
            'value': str(self.StartSAMULimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartSAMULimitTable))
        })

        for samu in range(self.StartSAMULimitTable_count):
            pos_samu = self.powerTablePosition + self.SAMULimitTableOffset + 2 + (samu * 5)
            self.data['Start SAMU limit table'].append({
                'name': 'DPM ' + str(BytesReader.read_int24(self.rom, pos_samu + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_samu)),
                'unit': 'mV',
                'position': str(hex(pos_samu))
            })

        # Start ACP limit tables

        self.pos_StartACPLimitTable = self.powerTablePosition + self.ACPLimitTableOffset + 1
        self.StartACPLimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartACPLimitTable)
        self.data['Start ACP limit table'].append({
            'name': 'Start ACP limit table count',
            'value': str(self.StartACPLimitTable_count),
            'unit': '',
            'position': str(hex(self.pos_StartACPLimitTable))
        })

        for acp in range(self.StartACPLimitTable_count):
            pos_acp = self.powerTablePosition + self.ACPLimitTableOffset + 2 + (acp * 5)
            self.data['Start ACP limit table'].append({
                'name': 'DPM ' + str(BytesReader.read_int24(self.rom, pos_acp + 2)),
                'value': str(BytesReader.read_int16(self.rom, pos_acp)),
                'unit': 'mV',
                'position': str(hex(pos_samu))
            })

        # Fan Profile

        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int8(self.rom, self.fanTablePosition + 1)),
            'unit': '°C',
            'position': str(hex(self.fanTablePosition + 1))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 2)),
            'unit': '/ 100 - °C',
            'position': str(hex(self.fanTablePosition + 2))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 4)),
            'unit': '/ 100 - °C',
            'position': str(hex(self.fanTablePosition + 4))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 6)),
            'unit': '/ 100 - °C',
            'position': str(hex(self.fanTablePosition + 6))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 8)),
            'unit': '/ 100 - %',
            'position': str(hex(self.fanTablePosition + 8))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 10)),
            'unit': '/ 100 - %',
            'position': str(hex(self.fanTablePosition + 10))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 12)),
            'unit': '/ 100 - %',
            'position': str(hex(self.fanTablePosition + 12))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int16(self.rom, self.fanTablePosition + 14)),
            'unit': '/ 100 - °C',
            'position': str(hex(self.fanTablePosition + 14))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int8(self.rom, self.fanTablePosition + 16)),
            'unit': '°C',
            'position': str(hex(self.fanTablePosition + 16))
        })
        self.data['Fan Profile'].append({
            'name': 'DPM',
            'value': str(BytesReader.read_int8(self.rom, self.fanTablePosition + 17)),
            'unit': '%',
            'position': str(hex(self.fanTablePosition + 17))
        })

        # VRM settings

        self.pos_vrmList_size = self.gpuVRMTablePosition + 6
        self.vrmList_size = BytesReader.read_int16(self.rom, self.pos_vrmList_size)
        self.data['VRM settings'].append({
            'name': 'VRM table count',
            'value': str(self.vrmList_size),
            'unit': '',
            'position': str(hex(self.pos_vrmList_size))
        })

        for vrm in range(2, self.vrmList_size, 2):
            pos_temp = self.gpuVRMTablePosition + 6 + vrm
            temp = BytesReader.read_int16(self.rom, pos_temp)
            if hex(temp) in vrm_types:
                value = BytesReader.read_int16(self.rom, self.gpuVRMTablePosition + 8 + vrm)
                self.data['VRM settings'].append({
                    'name': vrm_types[hex(temp)],
                    'value': str(value),
                    'unit': '',
                    'position': str(hex(pos_temp))
                })
            else:
                print('unknow VRM :', hex(temp), '@', hex(pos_temp))

