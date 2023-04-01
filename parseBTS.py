import pandas as pd
import numpy as np
import sys

gPrefix="//bulkCmConfigDataFile/configData/class"
gRow="/Item"

def formXPath(model="", function=""):
    if(len(model) == 0 or len(function) == 0):
       return gPrefix
    else:
       function = function + "_" + model
       return gPrefix+"[@name='"+model+"']/object/class[@name='"+function+"']/object/parameter"

def createXSLT(function):
    templateFile='tab_template.xslt'
    with open(templateFile, 'r') as file:
       data = file.read()
       data = data.replace('PREFIX', gPrefix)
       data = data.replace('FUNCTION', function)
    genTmplFile="tab_"+function+".xslt"
    with open(genTmplFile, 'w') as file:
       file.write(data)
    return genTmplFile

def fetchConfigBTS(func, model, attrib_arr):
    xpath=formXPath(model, func)
    df = pd.read_xml(fname, xpath=xpath)
#    print(df)
    df1 = df[df['name'].isin(attrib_arr)]
    print(df1)

def fetchConfigBTSArr(func, model, key, attrib_arr):
    sltfname = createXSLT(func + "_" + model)
    xpath=gRow
    df = pd.read_xml(fname, xpath=xpath, stylesheet=sltfname)
#    print(df)
    df = df.set_index(key)
    df1 = df[attrib_arr]
    print(df1)
    return df1
    
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
    xpath = formXPath()
#    xpath="//bulkCmConfigDataFile/configData/class"
    df = pd.read_xml(fname, xpath=xpath)
    print("input file is of device "+df.loc[0]['name'])
    return df.loc[0]['name']

def print_usage():
   print("Usage: python3 "+sys.argv[0]+" <filename_to_parse>")

if len(sys.argv) < 2:
   print_usage()
   exit()

fname = sys.argv[1]
devType = identifyDevice(fname)
if devType.startswith('BTS'):
   fetchConfigBTS('NODE', devType, ['NODEID', 'NODENAME'])
   fetchConfigBTS('CNOPERATOR', devType, ['CNOPERATORNAME', 'MCC', 'MNC'])
   fetchConfigBTS('LOCATION', devType, ['LOCATIONTYPE', 'REGION', 'CITY', 'ADDRESS', 'LATITUDEDEGFORMAT', 'LONGITUDEDEGFORMAT'])
   fetchConfigBTSArr('CELL', devType, 'CELLID', ["CELLNAME", "ENODEBFUNCTIONNAME", "CELLRADIUS", "FREQBAND", "PHYCELLID", "TXRXMODE"])
   fetchConfigBTSArr('GERANNCELL', devType, 'LOCALCELLID', ['LAC', 'MCC', 'MNC', 'LOCALCELLNAME', 'ENODEBFUNCTIONNAME'])
   fetchConfigBTSArr('UTRANNCELL', devType, 'LOCALCELLID', ['RNCID', 'MCC', 'MNC', 'LOCALCELLNAME', 'ENODEBFUNCTIONNAME'])
   fetchConfigBTSArr('NRCELL', devType, 'NRCELLID', ['CELLID', 'CELLNAME', 'GNODEBFUNCTIONNAME', 'FREQUENCYBAND'])
elif "RNC" in devType:
   fetchConfigRNC()
else:
   print("unknown network element = " + df.type)
   print("exiting...")

