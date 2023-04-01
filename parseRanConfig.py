import pandas as pd
import numpy as np
import sys

hwns = {"h" : "http://www.huawei.com/specs/SOM", "xsi" : "http://www.w3.org/2001/XMLSchema-instance"}
fname = "GNBIExport_XML_RT_09_23_2022_13_25_50_455_10_168_194_11.xml"
#fname = "UNBIExport_XML_RT_09_23_2022_13_25_49_886_10_168_194_11.xml"

def fetchParams(moi, attribs):
    module_type="Radio"
    obj=moi
    xpath="//h:module[@xsi:type='"+module_type+"']/h:moi[@xsi:type='"+obj+"']/h:attributes"
#    print(xpath)
    df = pd.read_xml(fname, xpath=xpath, namespaces=hwns)
#    print(df)
    df1 = df.loc[0][attribs]
    return df1
    
def fetchDeviceSummary():
    module_type="Transmission"
    obj="SYS"
    xpath="//h:module[@xsi:type='"+module_type+"']/h:moi[@xsi:type='"+obj+"']/h:attributes"
    df = pd.read_xml(fname, xpath=xpath, namespaces=hwns)
#    print(df)
    print("Device:"+df.loc[0]['SYSOBJECTID']+" at "+df.loc[0]['SYSLOCATION']+" model "+df.loc[0]['SYSDESC'])
    
def fetchConfig1(obj, key, attrib_arr, in_radio=0):
    module_type="Transmission"
    if in_radio==1:
        module_type="Radio"
    xpath="//h:module[@xsi:type='"+module_type+"']/h:moi[@xsi:type='"+obj+"']/h:attributes"
    df = pd.read_xml(fname, xpath=xpath, namespaces=hwns)
    df = df.set_index(key)
    df1 = df[attrib_arr]
#    print(df1)
    print("Fetching "+obj+"...")
#    print(df1.to_csv())
    return df1

def fetchConfig(obj, in_radio=0):
    module_type="Transmission"
    if in_radio==1:
        module_type="Radio"
    xpath="//h:module[@xsi:type='"+module_type+"']/h:moi[@xsi:type='"+obj+"']/h:attributes"
    df = pd.read_xml(fname, xpath=xpath, namespaces=hwns)
#    print(df)
    print(obj)
    print(df.to_csv())

def fetchConfigBSC():
    bts = fetchConfig1("BTS", "BTSID", ["BTSNAME", "BTSDESC"], 0)
    cells = fetchConfig1("GCELL", "CELLID", ["CELLNAME", "LAC", "CI", "MCC", "MNC", "NCC", "BCC"], 0)
    locations = fetchConfig1("GCELLLCS", "CELLID", ["LATIINT", "LATIDECI", "LONGIINT", "LONGIDECI"], 1)
    freq = fetchConfig1("GCELLFREQ", "CELLID", ["FREQ1", "FREQ2", "FREQ3"])
    cell2bts = fetchConfig1("CELLBIND2BTS", "CELLID", ["BTSID"])
    cell2bts1 = pd.merge(cell2bts, bts, how='inner', right_index=True, left_on='BTSID')
#    print(cell2bts1)
    all_config = pd.concat([cell2bts1, cells, locations, freq], axis=1)
    print(all_config.to_csv())
#    fetchConfig("GTRX")

def fetchConfigRNC():
    nodeb = fetchConfig1("NODEBEQUIPMENT", "NODEBID", ["NODEBNAME", "SERIES"], 0)
#    print(nodeb)
    cells = fetchConfig1("UCELL", "CELLID", ["CELLNAME", "NODEBNAME", "RAC", "SAC", "LAC"], 1)
    mnc_mcc = fetchParams("UCNOPERATOR", ["MCC", "MNC"])
    cells["MCC"] = mnc_mcc["MCC"]
    cells["MNC"] = mnc_mcc["MNC"]
#    fetchConfig("ULTECELL", 1)
    locations = fetchConfig1("USMLCCELL", "CELLID", ["ANTENNALATITUDEDEGREE", "ANTENNALONGITUDEDEGREE"], 1)
    all_config = pd.concat([cells, locations], axis=1)
    print(all_config.to_csv())
#    fetchConfig("GCELLFREQ")
#    fetchConfig("GTRX")

def identifyDevice(fname):
    xpath="//h:NE"
    df = pd.read_xml(fname, xpath=xpath, namespaces=hwns)
    print("input file is of device "+df.loc[0]['type'])
    return df.loc[0]['type']
    if "BSC" in df.loc[0]['type']:
       fetchConfigBSC()
    elif "RNC" in df.loc[0]['type']:
       fetchConfigRNC()
    else:
       print("unknown network element = " + df.type)
       print("exiting...")

def print_usage():
   print("Usage: python3 "+sys.argv[0]+" <filename_to_parse>")

if len(sys.argv) < 2:
   print_usage()
   exit()

fname = sys.argv[1]
devType = identifyDevice(fname)
fetchDeviceSummary()
if "BSC" in devType:
   fetchConfigBSC()
elif "RNC" in devType:
   fetchConfigRNC()
else:
   print("unknown network element = " + df.type)
   print("exiting...")

