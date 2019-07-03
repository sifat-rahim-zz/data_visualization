
#!/usr/bin/env python

# Author : hello_sifat@yahoo.com, sifat@telenorhealth.com
# Date : 06 Aug, 2017
# This scripts generates two files, nodes.json, links.json (needed for D3 JS)
# How to check this script : python script_name

import yaml     # if not installed: sudo pip install PyYAML
import sys
import json
import psycopg2
import psycopg2.extras
from pprint import pprint
from datetime import datetime, date, timedelta
from collections import OrderedDict


today = date.today()   # a datetime.date object
yesterday = ( date.today() - timedelta(1) )

db = 'local_postgres'

try :
    fp = open('config.txt','r')
    config_dict = json.load(fp)
    host = config_dict[db]['host']
    db_name = config_dict[db]['db_name']
    user = config_dict[db]['user']
    password = config_dict[db]['password']
except Exception, e:
    print str(e)
    print "!!ERROR!!, config file load ERROR!!.. exiting program.."
    sys.exit(0)

conn_string = "host='{host}' dbname='{db_name}' user='{user}' password='{password}'".format(host=host,db_name=db_name,user=user,password=password)
conn = psycopg2.connect(conn_string)

# execute an sql query, and simply return fetchall result.
def exec_sql_general(sql_str) :
    try :
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(sql_str) #print sql_res
        sql_res = cursor.fetchall()
    except Exception, e:
        print 'DB conn problem', str(e)
        #sys.exit(0)
    finally:
        cursor.close()

    return sql_res  # returns the whole resut, now we need to read row by row



def create_nodes_json(d) :
    ''' created nodes.json file '''

    fp = open('nodes.json','w')
    str = '[ '+'\n'
    for k,v in d.iteritems():
        str += ''' {{ "name": "{k}", "id": {v} }} '''.format(k=k,v=v)
        str += ',\n'
    str = str[:-2]
    str += '\n]'
    fp.write(str)


def create_links_json(l) :
    ''' created links.json file '''

    color_dict_link = {"YES": "#beda96", "NO" : "#f90804"}  # #beda96 , #bad0c4

    fp = open('links.json','w')
    str = '[ '+'\n'
    for i in l:
        j = i.strip().encode('ascii','ignore').split('---')

        str += ''' {{ "source": {s} , "target": {t}, "color_val": "{c}" }} '''.format( s=dict_nodes[ j[0] ], t=dict_nodes[ j[1] ] ,c=color_dict_link[ j[2] ])
        str += ',\n'
    str = str[:-2]
    str += '\n]'
    fp.write(str)




if __name__ == '__main__' :

    sql_str = '''SELECT DISTINCT service_name FROM daily_nagios_check WHERE DATE(day_date_time)='{report_date}' '''.format(report_date=yesterday)
    res_str = exec_sql_general(sql_str) #; print sql_str
    curr_service_list = [ i[0] for i in res_str ] #; print curr_service_list #; sys.exit(0)

    '''
    DR_APPOINTMENT
    DOCTOR_CHAT
    CORE_API
    NAVIGATOR
    TONICAPP_BACKEND
    BILLING
    CARROTCAKE
    CONCEPT_MANAGER
    CASTRO
    WEBSITE
    '''
    list_links = []
    dict_tmp = {}
    dict_nodes = OrderedDict()   # dict of all nodes
    node_id = 0

    for i in curr_service_list :
        if i not in dict_nodes.keys():
            dict_nodes[i] = node_id
            node_id += 1
        #print dict_nodes

        # getting components from last successful result
        sql_str = '''SELECT
        daily_nagios_check.info #>> '{{status}}'
        FROM
            daily_nagios_check
        WHERE service_name = '{service_name}'
            --AND DATE(day_date_time) = '{report_date}'
            AND daily_nagios_check.info #>> '{{message}}' IN ('OK','ERROR')
        ORDER BY day_date_time
        DESC LIMIT 1 '''.format(service_name=i,report_date=yesterday)
        #print i, sql_str #; sys.exit(0)
        res_str = exec_sql_general(sql_str)

        dict_tmp = json.loads(res_str[0][0])  # sample dict_tmp for CASTRO is {"CAAS": "YES", "TH_SMSC": "YES", "CORE_API": "YES", "TONICAPP_BACKEND": "YES"}
        #print i, 'kk', dict_tmp #; sys.exit(0)
        for j in dict_tmp.keys(): # j is dependency-microservice
            curr_str = i + '---' + j.encode('ascii','ignore') + '---' + dict_tmp[j]
            #print curr_str #; sys.exit(0)
            list_links.append(curr_str)
            if j.encode('ascii','ignore') not in dict_nodes.keys():
                dict_nodes[j.encode('ascii','ignore')] = node_id
                node_id += 1
                #print i, dict_tmp

    #pprint(dict_nodes)
    #print list_links , len(list_links)

    create_nodes_json(dict_nodes)
    create_links_json(list_links)
