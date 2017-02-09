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

    def __init__(rom: bytes):
        self.rom = rom
        self.parse()

    def parse(self):
        print('parsing rom')

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

        self.pos_biosName = 220
        self.biosName = BytesReader.read_str(self.rom, self.pos_biosName, 32)
        print('biosName :', self.biosName)

        self.pos_devIDstr = 6 + self.pciInfoPosition
        self.devIDstr = hex(BytesReader.read_int16(self.rom, self.pos_devIDstr))
        print('devIDstr :', self.devIDstr)

        self.pos_vendorID = 4 + self.pciInfoPosition
        self.vendorID = hex(BytesReader.read_int16(self.rom, self.pos_vendorID))
        print('vendorID :', self.vendorID)

        self.pos_productData = 8 + self.pciInfoPosition
        self.productData = hex(BytesReader.read_int16(self.rom, self.pos_productData))
        print('productData :', self.productData)

        self.pos_structureLength = 10 + self.pciInfoPosition
        self.structureLength = hex(BytesReader.read_int16(self.rom, self.pos_structureLength))
        print('structureLength :', self.structureLength)

        self.pos_structureRevision = 12 + self.pciInfoPosition
        self.structureRevision = hex(BytesReader.read_int8(self.rom, self.pos_structureRevision))
        print('structureRevision :', self.structureRevision)

        self.pos1_classCode = 13 + self.pciInfoPosition
        self.pos2_classCode = 14 + self.pciInfoPosition
        self.pos3_classCode = 15 + self.pciInfoPosition
        self.classCode = hex(BytesReader.read_int8(self.rom, self.pos1_classCode)) + ' - ' \
                         + hex(BytesReader.read_int8(self.rom, self.pos2_classCode)) + ' - ' \
                         + hex(BytesReader.read_int8(self.rom, self.pos3_classCode))
        print('classCode :', self.classCode)

        self.pos_imageLength = 16 + self.pciInfoPosition
        self.imageLength = hex(BytesReader.read_int16(self.rom, self.pos_imageLength))
        print('imageLength :', self.imageLength)

        self.pos_revisionLevel = 18 + self.pciInfoPosition
        self.revisionLevel = hex(BytesReader.read_int16(self.rom, self.pos_revisionLevel))
        print('revisionLevel :', self.revisionLevel)

        self.pos_codeType = 20 + self.pciInfoPosition
        self.codeType = hex(BytesReader.read_int8(self.rom, self.pos_codeType))
        print('codeType :', self.codeType)

        self.pos_indicator = 21 + self.pciInfoPosition
        self.indicator = hex(BytesReader.read_int8(self.rom, self.pos_indicator))
        print('indicator :', self.indicator)

        self.pos_reserved = 22 + self.pciInfoPosition
        self.reserved = hex(BytesReader.read_int16(self.rom, self.pos_reserved))
        print('reserved :', self.reserved)

        if self.devIDstr in supportedDevIDs:
            print('>> Ok this rom device is supported')
        else:
            print('>> Nok this rom device is not supported, exiting')
            exit(-1)

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

        self.pos_SSVID = self.pciInfoPosition - 12
        self.SSVID = hex(BytesReader.read_int16(self.rom, self.pos_SSVID))[2:]
        print('SSVID :', self.SSVID)

        self.pos_SSDID = self.pciInfoPosition - 14
        self.SSVID = hex(BytesReader.read_int16(self.rom, self.pos_SSDID))[2:]
        print('SSVID :', self.SSVID)

        self.pos_CCCLimitsPosition = 44 + self.powerTablePosition
        self.CCCLimitsPosition = self.powerTablePosition + BytesReader.read_int16(self.rom, self.pos_CCCLimitsPosition)
        print('CCCLimitsPosition :', hex(self.CCCLimitsPosition))

        self.pos_gpuMaxClock = self.CCCLimitsPosition + 2
        self.gpuMaxClock = BytesReader.read_int24(self.rom, self.pos_gpuMaxClock)
        print('gpuMaxClock :', self.gpuMaxClock / 100, 'MHz')

        self.pos_memMaxClock = self.CCCLimitsPosition + 6
        self.memMaxClock = BytesReader.read_int24(self.rom, self.pos_memMaxClock)
        print('memMaxClock :', self.memMaxClock / 100, 'MHz')

        temp_pos = self.powerTablePosition + self.clockInfoOffset
        self.gpumemFrequencyListAndPowerLimit = {
            hex(temp_pos + 2):
                str(BytesReader.read_int24(self.rom, temp_pos + 2) / 100) + ' MHz',
            hex(temp_pos + 11):
                str(BytesReader.read_int24(self.rom, temp_pos + 11) / 100) + ' MHz',
            hex(temp_pos + 20):
                str(BytesReader.read_int24(self.rom, temp_pos + 20) / 100) + ' MHz',
            hex(temp_pos + 5):
                str(BytesReader.read_int24(self.rom, temp_pos + 5) / 100) + ' MHz',
            hex(temp_pos + 14):
                str(BytesReader.read_int24(self.rom, temp_pos + 14) / 100) + ' MHz',
            hex(temp_pos + 23):
                str(BytesReader.read_int24(self.rom, temp_pos + 23) / 100) + ' MHz',

            hex(self.powerTablePosition + self.tdpLimitOffset):
                str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.tdpLimitOffset)) + ' W',
            hex(self.powerTablePosition + self.powerDeliveryLimitOffset):
                str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset)) + ' W',

            hex(self.powerTablePosition + self.tdcLimitOffset):
                str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.tdcLimitOffset)) + ' A',

            hex(self.powerTablePosition + self.powerDeliveryLimitOffset + 2):
                str(BytesReader.read_int16(self.rom, self.powerTablePosition + self.powerDeliveryLimitOffset + 2)) + ' °C',
        }
        pprint(self.gpumemFrequencyListAndPowerLimit)

        self.pos_vddciTableCount = self.powerTablePosition + self.AUXvoltageOffset
        self.vddciTableCount = BytesReader.read_int8(self.rom, self.pos_vddciTableCount)
        print('vddciTableCount :', self.vddciTableCount)

        self.VDDCITable = []
        for vddcicounter in range(self.vddciTableCount):
            pos_vddci = self.powerTablePosition + self.AUXvoltageOffset + 1 + (vddcicounter * 5)
            self.VDDCITable.append(str(BytesReader.read_int24(self.rom, pos_vddci) / 100) + ' MHz')
        print('VDDCITable :')
        pprint(self.VDDCITable)

        self.pos_memoryFrequencyTableCount = self.powerTablePosition + self.memoryFrequencyTableOffset
        self.memoryFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_memoryFrequencyTableCount)
        print('gpuFrequencyTableCount :', self.memoryFrequencyTableCount)

        self.MEMFreqTable = []
        for pos_mem_freq in range(self.memoryFrequencyTableCount):
            pos_mem_freq = self.powerTablePosition + self.memoryFrequencyTableOffset + 1 + (pos_mem_freq * 5)
            self.MEMFreqTable.append(str(BytesReader.read_int24(self.rom, pos_mem_freq) / 100) + ' MHz')
        print('MEMFreqTable :')
        pprint(self.MEMFreqTable)

        self.pos_gpuFrequencyTableCount = self.powerTablePosition + self.gpuFrequencyTableOffset
        self.gpuFrequencyTableCount = BytesReader.read_int8(self.rom, self.pos_gpuFrequencyTableCount)
        print('gpuFrequencyTableCount :', self.gpuFrequencyTableCount)

        self.GPUFreqTable = []
        for gpu_freq_counter in range(self.gpuFrequencyTableCount):
            pos_gpu_freq = self.powerTablePosition + self.gpuFrequencyTableOffset + 1 + (gpu_freq_counter * 5)
            self.GPUFreqTable.append(str(BytesReader.read_int24(self.rom, pos_gpu_freq) / 100) + ' MHz')
        print('GPUFreqTable :')
        pprint(self.GPUFreqTable)

        self.pos_StartVCELimitTable = self.powerTablePosition + self.VCELimitTableOffset
        self.StartVCELimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartVCELimitTable)
        self.StartVCELimitTable = {}
        for vce in range(self.StartVCELimitTable_count):
            pos_vce = self.powerTablePosition + self.VCELimitTableOffset + 1 + (vce * 3)
            self.StartVCELimitTable[hex(pos_vce)] = str(BytesReader.read_int8(self.rom, pos_vce + 2)) + ' DPM, ' \
                                                    + str(BytesReader.read_int16(self.rom, pos_vce)) + ' mV'
        print('StartVCELimitTable :')
        pprint(self.StartVCELimitTable)

        self.pos_StartUVDLimitTable = self.powerTablePosition + self.UVDLimitTableOffset
        self.StartUVDLimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartUVDLimitTable)
        self.StartUVDLimitTable = {}
        for uvd in range(self.StartUVDLimitTable_count):
            pos_uvd = self.powerTablePosition + self.UVDLimitTableOffset + 1 + (uvd * 3)
            self.StartUVDLimitTable[hex(pos_uvd)] = str(BytesReader.read_int8(self.rom, pos_uvd + 2)) + ' DPM, ' \
                                                    + str(BytesReader.read_int16(self.rom, pos_uvd)) + ' mV'
        print('StartUVDLimitTable :')
        pprint(self.StartUVDLimitTable)

        self.pos_StartSAMULimitTable = self.powerTablePosition + self.SAMULimitTableOffset + 1
        self.StartSAMULimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartSAMULimitTable)
        self.StartSAMULimitTable = {}
        for samu in range(self.StartSAMULimitTable_count):
            pos_samu = self.powerTablePosition + self.SAMULimitTableOffset + 2 + (samu * 5)
            self.StartSAMULimitTable[hex(pos_samu)] = str(BytesReader.read_int24(self.rom, pos_samu + 2)) + ' DPM, ' \
                                                      + str(BytesReader.read_int16(self.rom, pos_samu)) + ' mV'
        print('StartSAMULimitTable :')
        pprint(self.StartSAMULimitTable)

        self.pos_StartACPLimitTable = self.powerTablePosition + self.ACPLimitTableOffset + 1
        self.StartACPLimitTable_count = BytesReader.read_int8(self.rom, self.pos_StartACPLimitTable)
        self.StartACPLimitTable = {}
        for acp in range(self.StartACPLimitTable_count):
            pos_acp = self.powerTablePosition + self.ACPLimitTableOffset + 2 + (acp * 5)
            self.StartACPLimitTable[hex(pos_acp)] = str(BytesReader.read_int24(self.rom, pos_acp + 2)) + ' DPM, ' \
                                                    + str(BytesReader.read_int16(self.rom, pos_acp)) + ' mV'
        print('StartACPLimitTable :')
        pprint(self.StartACPLimitTable)

        self.fanList = {
            hex(self.fanTablePosition + 1): str(BytesReader.read_int8(self.rom, self.fanTablePosition + 1)) + ' °C',
            hex(self.fanTablePosition + 2): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 2) / 100) + ' °C',
            hex(self.fanTablePosition + 4): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 4) / 100) + ' °C',
            hex(self.fanTablePosition + 6): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 6) / 100) + ' °C',
            hex(self.fanTablePosition + 8): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 8) / 100) + ' %',
            hex(self.fanTablePosition + 10): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 10) / 100) + ' %',
            hex(self.fanTablePosition + 12): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 12) / 100) + ' %',
            hex(self.fanTablePosition + 14): str(BytesReader.read_int16(self.rom, self.fanTablePosition + 14) / 100) + ' °C',
            hex(self.fanTablePosition + 16): str(BytesReader.read_int8(self.rom, self.fanTablePosition + 16)) + ' °C',
            hex(self.fanTablePosition + 17): str(BytesReader.read_int8(self.rom, self.fanTablePosition + 17)) + ' %',
        }
        print('fanList :')
        pprint(self.fanList)

        self.pos_vrmList_size = self.gpuVRMTablePosition + 6
        self.vrmList_size = BytesReader.read_int16(self.rom, self.pos_vrmList_size)
        self.vrmList = {}
        for vrm in range(2, self.vrmList_size, 2):
            pos_temp = self.gpuVRMTablePosition + 6 + vrm
            temp = BytesReader.read_int16(self.rom, pos_temp)
            if hex(temp) in vrm_types:
                value = BytesReader.read_int16(self.rom, self.gpuVRMTablePosition + 8 + vrm)
                self.vrmList[vrm_types[hex(temp)] + ' @' + hex(pos_temp)] = value
        print('vrmList :')
        pprint(self.vrmList)
