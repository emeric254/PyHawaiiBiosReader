#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from tools import RomReader, BytesReader

supportedDevIDs = {'0x67a0', '0x67a1', '0x67a2', '0x67a8', '0x67a9', '0x67aa', '0x67b0', '0x67b1', '0x67b9'}
vrm_types = {'0x22': 'fsw 1 VDDC', '0x23': 'fsw 2 VDDI', '0x26': 'hidden VDDC/VDDCI',
             '0x33': 'Voltage Protection', '0x34': 'Current Protection', '0x38': 'LLC',
             '0x3d': 'VDDCR Limit', '0x8d': 'VDDC Offset', '0x8e': 'VDDCI Offset'}

rom_bytes = RomReader.read_rom('290X_NOMOD_STOCK_V1.8.rom')
# print(rom_bytes)

pos_pciInfoPosition = 24
pciInfoPosition = BytesReader.read_int16(rom_bytes, pos_pciInfoPosition)
print('pciInfoPosition :', hex(pciInfoPosition))

pos_headerPosition = 72
headerPosition = BytesReader.read_int16(rom_bytes, pos_headerPosition)
print('headerPosition :', hex(headerPosition))

pos_dataPointersPosition = 32 + headerPosition
dataPointersPosition = BytesReader.read_int16(rom_bytes, pos_dataPointersPosition)
print('dataPointersPosition :', hex(dataPointersPosition))

pos_powerTablePosition = 34 + dataPointersPosition
powerTablePosition = BytesReader.read_int16(rom_bytes, pos_powerTablePosition)
print('powerTablePosition :', hex(powerTablePosition))

pos_gpuVRMTablePosition = 68 + dataPointersPosition
gpuVRMTablePosition = BytesReader.read_int16(rom_bytes, pos_gpuVRMTablePosition)
print('gpuVRMTablePosition :', hex(gpuVRMTablePosition))

pos_biosName = 220
biosName = BytesReader.read_str(rom_bytes, pos_biosName, 32)
print('biosName :', biosName)

pos_devIDstr = 6 + pciInfoPosition
devIDstr = hex(BytesReader.read_int16(rom_bytes, pos_devIDstr))
print('devIDstr :', devIDstr)

pos_vendorID = 4 + pciInfoPosition
vendorID = hex(BytesReader.read_int16(rom_bytes, pos_vendorID))
print('vendorID :', vendorID)

pos_productData = 8 + pciInfoPosition
productData = hex(BytesReader.read_int16(rom_bytes, pos_productData))
print('productData :', productData)

pos_structureLenght = 10 + pciInfoPosition
structureLenght = hex(BytesReader.read_int16(rom_bytes, pos_structureLenght))
print('structureLenght :', structureLenght)

pos_structureRevision = 12 + pciInfoPosition
structureRevision = hex(BytesReader.read_int8(rom_bytes, pos_structureRevision))
print('structureRevision :', structureRevision)

pos1_classCode = 13 + pciInfoPosition
pos2_classCode = 14 + pciInfoPosition
pos3_classCode = 15 + pciInfoPosition
classCode = hex(BytesReader.read_int8(rom_bytes, pos1_classCode)) + ' - ' \
            + hex(BytesReader.read_int8(rom_bytes, pos2_classCode)) + ' - ' \
            + hex(BytesReader.read_int8(rom_bytes, pos3_classCode))
print('classCode :', classCode)

pos_imageLenght = 16 + pciInfoPosition
imageLenght = hex(BytesReader.read_int16(rom_bytes, pos_imageLenght))
print('imageLenght :', imageLenght)

pos_revisionLevel = 18 + pciInfoPosition
revisionLevel = hex(BytesReader.read_int16(rom_bytes, pos_revisionLevel))
print('revisionLevel :', revisionLevel)

pos_codeType = 20 + pciInfoPosition
codeType = hex(BytesReader.read_int8(rom_bytes, pos_codeType))
print('codeType :', codeType)

pos_indicator = 21 + pciInfoPosition
indicator = hex(BytesReader.read_int8(rom_bytes, pos_indicator))
print('indicator :', indicator)

pos_reserved = 22 + pciInfoPosition
reserved = hex(BytesReader.read_int16(rom_bytes, pos_reserved))
print('reserved :', reserved)

if devIDstr in supportedDevIDs:
    print('>> Ok this rom device is supported')
else:
    print('>> Nok this rom device is not supported, exiting')
    exit(-1)

powerTableSize = BytesReader.read_int16(rom_bytes, powerTablePosition)
print('powerTableSize :', powerTableSize)

pos_clockInfoOffset = 11 + powerTablePosition
clockInfoOffset = BytesReader.read_int16(rom_bytes, pos_clockInfoOffset)
print('clockInfoOffset :', hex(clockInfoOffset))

pos_fanTablePosition = 42 + powerTablePosition
fanTablePosition = powerTablePosition + BytesReader.read_int16(rom_bytes, pos_fanTablePosition)
print('fanTablePosition :', hex(fanTablePosition))

pos_gpuFrequencyTableOffset = 54 + powerTablePosition
gpuFrequencyTableOffset = BytesReader.read_int16(rom_bytes, pos_gpuFrequencyTableOffset)
print('gpuFrequencyTableOffset :', hex(gpuFrequencyTableOffset))

# TEMP (Only gets first VDDCI) - +4 to skip number of vddci states(1 byte) and first frequency(3 bytes)
pos_AUXvoltageOffset = 56 + powerTablePosition
AUXvoltageOffset = BytesReader.read_int16(rom_bytes, pos_AUXvoltageOffset)
print('AUXvoltageOffset :', hex(AUXvoltageOffset))

pos_memoryFrequencyTableOffset = 58 + powerTablePosition
memoryFrequencyTableOffset = BytesReader.read_int16(rom_bytes, pos_memoryFrequencyTableOffset)
print('memoryFrequencyTableOffset :', hex(memoryFrequencyTableOffset))

pos_limitsPointersOffset = 44 + powerTablePosition
limitsPointersOffset = BytesReader.read_int16(rom_bytes, pos_limitsPointersOffset)
print('limitsPointersOffset :', hex(limitsPointersOffset))

pos_VCETableOffset = 10 + limitsPointersOffset + powerTablePosition
VCETableOffset = BytesReader.read_int16(rom_bytes, pos_VCETableOffset)
print('VCETableOffset :', hex(VCETableOffset))

pos_VCEunknownStatesNum = 1 + VCETableOffset + powerTablePosition
VCEunknownStatesNum = BytesReader.read_int8(rom_bytes, pos_VCEunknownStatesNum)
print('VCEunknownStatesNum :', hex(VCEunknownStatesNum))

VCELimitTableOffset = VCETableOffset + 2 + VCEunknownStatesNum * 6
print('VCELimitTableOffset :', hex(VCELimitTableOffset))

pos_UVDTableOffset = 12 + powerTablePosition + limitsPointersOffset
UVDTableOffset = BytesReader.read_int16(rom_bytes, pos_UVDTableOffset)
print('UVDTableOffset :', hex(UVDTableOffset))

pos_UVDunknownStatesNum = 1 + powerTablePosition + UVDTableOffset
UVDunknownStatesNum = BytesReader.read_int8(rom_bytes, pos_UVDunknownStatesNum)
print('UVDunknownStatesNum :', hex(UVDunknownStatesNum))

UVDLimitTableOffset = UVDTableOffset + 2 + UVDunknownStatesNum * 6
print('UVDLimitTableOffset :', hex(UVDLimitTableOffset))

pos_SAMULimitTableOffset = 14 + powerTablePosition + limitsPointersOffset
SAMULimitTableOffset = BytesReader.read_int16(rom_bytes, pos_SAMULimitTableOffset)
print('SAMULimitTableOffset :', hex(SAMULimitTableOffset))

pos_ACPLimitTableOffset = 18 + powerTablePosition + limitsPointersOffset
ACPLimitTableOffset = BytesReader.read_int16(rom_bytes, pos_ACPLimitTableOffset)
print('ACPLimitTableOffset :', hex(ACPLimitTableOffset))

pos_tdpLimitOffset = 20 + powerTablePosition + limitsPointersOffset
tdpLimitOffset = 3 + BytesReader.read_int16(rom_bytes, pos_tdpLimitOffset)
print('tdpLimitOffset :', hex(tdpLimitOffset))

powerDeliveryLimitOffset = tdpLimitOffset + 12
print('powerDeliveryLimitOffset :', hex(powerDeliveryLimitOffset))

tdcLimitOffset = tdpLimitOffset + 2
print('tdcLimitOffset :', hex(tdcLimitOffset))

pos_SSVID = pciInfoPosition - 12
SSVID = hex(BytesReader.read_int16(rom_bytes, pos_SSVID))[2:]
print('SSVID :', SSVID)

pos_SSDID = pciInfoPosition - 14
SSVID = hex(BytesReader.read_int16(rom_bytes, pos_SSDID))[2:]
print('SSVID :', SSVID)

pos_CCCLimitsPosition = 44 + powerTablePosition
CCCLimitsPosition = powerTablePosition + BytesReader.read_int16(rom_bytes, pos_CCCLimitsPosition)
print('CCCLimitsPosition :', hex(CCCLimitsPosition))

pos_gpuMaxClock = CCCLimitsPosition + 2
gpuMaxClock = BytesReader.read_int24(rom_bytes, pos_gpuMaxClock)
print('gpuMaxClock :', gpuMaxClock / 100, 'MHz')

pos_memMaxClock = CCCLimitsPosition + 6
memMaxClock = BytesReader.read_int24(rom_bytes, pos_memMaxClock)
print('memMaxClock :', memMaxClock / 100, 'MHz')

gpumemFrequencyListAndPowerLimit = {
    hex(powerTablePosition + clockInfoOffset + 2):
        str(BytesReader.read_int24(rom_bytes, powerTablePosition + clockInfoOffset + 2) / 100) + ' MHz',
    hex(powerTablePosition + clockInfoOffset + 11):
        str(BytesReader.read_int24(rom_bytes, powerTablePosition + clockInfoOffset + 11) / 100) + ' MHz',
    hex(powerTablePosition + clockInfoOffset + 20):
        str(BytesReader.read_int24(rom_bytes, powerTablePosition + clockInfoOffset + 20) / 100) + ' MHz',
    hex(powerTablePosition + clockInfoOffset + 5):
        str(BytesReader.read_int24(rom_bytes, powerTablePosition + clockInfoOffset + 5) / 100) + ' MHz',
    hex(powerTablePosition + clockInfoOffset + 14):
        str(BytesReader.read_int24(rom_bytes, powerTablePosition + clockInfoOffset + 14) / 100) + ' MHz',
    hex(powerTablePosition + clockInfoOffset + 23):
        str(BytesReader.read_int24(rom_bytes, powerTablePosition + clockInfoOffset + 23) / 100) + ' MHz',

    hex(powerTablePosition + tdpLimitOffset):
        str(BytesReader.read_int16(rom_bytes, powerTablePosition + tdpLimitOffset)) + ' W',
    hex(powerTablePosition + powerDeliveryLimitOffset):
        str(BytesReader.read_int16(rom_bytes, powerTablePosition + powerDeliveryLimitOffset)) + ' W',

    hex(powerTablePosition + tdcLimitOffset):
        str(BytesReader.read_int16(rom_bytes, powerTablePosition + tdcLimitOffset)) + ' A',

    hex(powerTablePosition + powerDeliveryLimitOffset + 2):
        str(BytesReader.read_int16(rom_bytes, powerTablePosition + powerDeliveryLimitOffset + 2)) + ' °C',
}
pprint(gpumemFrequencyListAndPowerLimit)

pos_vddciTableCount = powerTablePosition + AUXvoltageOffset
vddciTableCount = BytesReader.read_int8(rom_bytes, pos_vddciTableCount)
print('vddciTableCount :', vddciTableCount)

VDDCITable = []
for vddcicounter in range(vddciTableCount):
    pos_vddci = powerTablePosition + AUXvoltageOffset + 1 + (vddcicounter * 5)
    VDDCITable.append(str(BytesReader.read_int24(rom_bytes, pos_vddci) / 100) + ' MHz')
print('VDDCITable :')
pprint(VDDCITable)

pos_memoryFrequencyTableCount = powerTablePosition + memoryFrequencyTableOffset
memoryFrequencyTableCount = BytesReader.read_int8(rom_bytes, pos_memoryFrequencyTableCount)
print('gpuFrequencyTableCount :', memoryFrequencyTableCount)

MEMFreqTable = []
for pos_mem_freq in range(memoryFrequencyTableCount):
    pos_mem_freq = powerTablePosition + memoryFrequencyTableOffset + 1 + (pos_mem_freq * 5)
    MEMFreqTable.append(str(BytesReader.read_int24(rom_bytes, pos_mem_freq) / 100) + ' MHz')
print('MEMFreqTable :')
pprint(MEMFreqTable)

pos_gpuFrequencyTableCount = powerTablePosition + gpuFrequencyTableOffset
gpuFrequencyTableCount = BytesReader.read_int8(rom_bytes, pos_gpuFrequencyTableCount)
print('gpuFrequencyTableCount :', gpuFrequencyTableCount)

GPUFreqTable = []
for gpu_freq_counter in range(gpuFrequencyTableCount):
    pos_gpu_freq = powerTablePosition + gpuFrequencyTableOffset + 1 + (gpu_freq_counter * 5)
    GPUFreqTable.append(str(BytesReader.read_int24(rom_bytes, pos_gpu_freq) / 100) + ' MHz')
print('GPUFreqTable :')
pprint(GPUFreqTable)

pos_StartVCELimitTable = powerTablePosition + VCELimitTableOffset
StartVCELimitTable_count = BytesReader.read_int8(rom_bytes, pos_StartVCELimitTable)
StartVCELimitTable = {}
for vce in range(StartVCELimitTable_count):
    pos_vce = powerTablePosition + VCELimitTableOffset + 1 + (vce * 3)
    StartVCELimitTable[hex(pos_vce)] = str(BytesReader.read_int8(rom_bytes, pos_vce + 2)) + ' DPM, ' \
                                       + str(BytesReader.read_int16(rom_bytes, pos_vce)) + ' mV'
print('StartVCELimitTable :')
pprint(StartVCELimitTable)

pos_StartUVDLimitTable = powerTablePosition + UVDLimitTableOffset
StartUVDLimitTable_count = BytesReader.read_int8(rom_bytes, pos_StartUVDLimitTable)
StartUVDLimitTable = {}
for uvd in range(StartUVDLimitTable_count):
    pos_uvd = powerTablePosition + UVDLimitTableOffset + 1 + (uvd * 3)
    StartUVDLimitTable[hex(pos_uvd)] = str(BytesReader.read_int8(rom_bytes, pos_uvd + 2)) + ' DPM, ' \
                                       + str(BytesReader.read_int16(rom_bytes, pos_uvd)) + ' mV'
print('StartUVDLimitTable :')
pprint(StartUVDLimitTable)

pos_StartSAMULimitTable = powerTablePosition + SAMULimitTableOffset + 1
StartSAMULimitTable_count = BytesReader.read_int8(rom_bytes, pos_StartSAMULimitTable)
StartSAMULimitTable = {}
for samu in range(StartSAMULimitTable_count):
    pos_samu = powerTablePosition + SAMULimitTableOffset + 2 + (samu * 5)
    StartSAMULimitTable[hex(pos_samu)] = str(BytesReader.read_int24(rom_bytes, pos_samu + 2)) + ' DPM, ' \
                                         + str(BytesReader.read_int16(rom_bytes, pos_samu)) + ' mV'
print('StartSAMULimitTable :')
pprint(StartSAMULimitTable)

pos_StartACPLimitTable = powerTablePosition + ACPLimitTableOffset + 1
StartACPLimitTable_count = BytesReader.read_int8(rom_bytes, pos_StartACPLimitTable)
StartACPLimitTable = {}
for acp in range(StartACPLimitTable_count):
    pos_acp = powerTablePosition + ACPLimitTableOffset + 2 + (acp * 5)
    StartACPLimitTable[hex(pos_acp)] = str(BytesReader.read_int24(rom_bytes, pos_acp + 2)) + ' DPM, ' \
                                       + str(BytesReader.read_int16(rom_bytes, pos_acp)) + ' mV'
print('StartACPLimitTable :')
pprint(StartACPLimitTable)

fanList = {
    hex(fanTablePosition + 1): str(BytesReader.read_int8(rom_bytes, fanTablePosition + 1)) + ' °C',
    hex(fanTablePosition + 2): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 2) / 100) + ' °C',
    hex(fanTablePosition + 4): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 4) / 100) + ' °C',
    hex(fanTablePosition + 6): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 6) / 100) + ' °C',
    hex(fanTablePosition + 8): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 8) / 100) + ' %',
    hex(fanTablePosition + 10): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 10) / 100) + ' %',
    hex(fanTablePosition + 12): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 12) / 100) + ' %',
    hex(fanTablePosition + 14): str(BytesReader.read_int16(rom_bytes, fanTablePosition + 14) / 100) + ' °C',
    hex(fanTablePosition + 16): str(BytesReader.read_int8(rom_bytes, fanTablePosition + 16)) + ' °C',
    hex(fanTablePosition + 17): str(BytesReader.read_int8(rom_bytes, fanTablePosition + 17)) + ' %',
}
print('fanList :')
pprint(fanList)

pos_vrmList_size = gpuVRMTablePosition + 6
vrmList_size = BytesReader.read_int16(rom_bytes, pos_vrmList_size)
vrmList = {}
for vrm in range(2, vrmList_size, 2):
    pos_temp = gpuVRMTablePosition + 6 + vrm
    temp = BytesReader.read_int16(rom_bytes, pos_temp)
    if hex(temp) in vrm_types:
        value = BytesReader.read_int16(rom_bytes, gpuVRMTablePosition + 8 + vrm)
        vrmList[vrm_types[hex(temp)] + ' @' + hex(pos_temp)] = value
print('vrmList :')
pprint(vrmList)
