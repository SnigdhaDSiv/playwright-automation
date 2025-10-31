#!/usr/bin/env python

import os, sys
from resources import resource_mapping
import json
from datetime import datetime
import json_diff
from src.utils.Logger import get_logger

logger = get_logger(__name__)

class DataAccessCompare:
    def __init__(self):
        self.dict = {}
      

    def data_convert_csv_new(self, array):
        stringfinal = ""
        for row in array:
            stringtmp = ""
            for elem in row:
                if ((type(elem) is int) or (type(elem) is float)):
                    string = str(elem)
                else:
                    string = '"{}"'.format(elem)
                if len(stringtmp) == 0:
                    stringtmp = stringtmp+string
                else:
                    stringtmp = stringtmp+','+string

                logger.log("OUT =>"+stringtmp)
            if len(stringfinal) == 0:
                stringfinal = stringfinal+stringtmp
            else:
                stringfinal = stringfinal+"\n"+stringtmp
        logger.log(stringfinal)
        return stringfinal


    def data_compare_same_keys(self,responsepayload, validatepayload):
        error = {}
        fail = False
        try:
            a, b = json.dumps(responsepayload, sort_keys=True), json.dumps(validatepayload, sort_keys=True)
            logger.log("data_compare_same_keys")
            logger.log(a)
            logger.log(b)
            if (a != b):
                fail = True
                error[0] = json_diff.diff(a,b)

        except (ValueError, KeyError, TypeError):
            print ("JSON format error")
        finally:
            return fail, error

    def data_compare(self,responsepayload, validatepayload, mapping):
        error = {}
        fail = False

        if not isinstance(responsepayload, type(validatepayload)):
            fail = True
            return fail, "error"
                          
        logger.info(type(responsepayload))
        logger.info (type(validatepayload))

        #responsepayload =  json.loads(respayload)
        #validatepayload =  json.dumps(validatepayload)

        #print(responsepayload['id'])
        #print(validatepayload['id'])

        str = "responsepayload key's {} value {}  does {} match validatepayload  key's {} value {}"
        try:
            # Access data
            for x in mapping['mapKey']:
                id_r = x.get("responsePayload")
                id_v = x.get("validatePayload")
                logger.info(id_r)
                if (x.get("validation") == "content"):
                    if (responsepayload.get(id_r) != validatepayload.get(id_v)):
                        fail = True
                        error[id_r] = str.format(id_r, responsepayload.get(id_r), "NOT", id_v, validatepayload.get(id_v))
                elif (x.get("validation") == "date"):
                    dtime1 = datetime.strptime(responsepayload['create_dt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    if (dtime1 != validatepayload['create_dt']):
                        fail = True
                        error[id_r] = str.format(id_r, responsepayload.get(id_r), "NOT", id_v, validatepayload.get(id_v))
        except (ValueError, KeyError, TypeError) as e:
            fail, error = True, e
        finally:
            return fail, error
    
    def data_compare_num(self,responepayload, validatepayload):
        fail = False
        error = {}
        print(str(responepayload) +"  "+str(validatepayload))
        try:
            if (responepayload != validatepayload):
                fail =  True
                error[0] = str(responepayload)+ " DOES NOT MATCH EXPECTED VALUE " + str(validatepayload)
        except (ValueError, KeyError, TypeError):
            print ("format error")
        finally:
            print (error)
            return fail, error


    def get_mapping_json(self, mappingkey):
         file = resource_mapping.validation_mapping[mappingkey]
         print(file)
         data = {}
         path = os.getcwd()
         path = os.path.join(path, 'resources')
         print(path)
         filename = os.path.join(path, file)
         print(filename)
         with open(str(filename), "r") as read_file:
             data = json.load(read_file)
         return data
    
   
