#! /usr/bin/python
#
'''
Project     :       Apache Solr Health Check
Version     :       0.1
Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Summary     :       This program is a nagios plugin that checks Apache Solr Health
Dependency  :       Linux/nagios/Python-2.6

Usage :
```````
shell> python check_solr.py
'''

#-----------------------|
# Import Python Modules |
#-----------------------|
import os, sys, urllib
from xml.dom import minidom
from optparse import OptionParser

#--------------------------|
# Main Program Starts Here |
#--------------------------|
# Command Line Arguments Parser
cmd_parser = OptionParser(version="%prog 0.1")
cmd_parser.add_option("-q", "--qps", action="store_true", dest="qps", help="Get QPS information of the SOLR Server")
cmd_parser.add_option("-d", "--doc", action="store_true", dest="doc", help="Get Docs information of the SOLR Server", default=True)
cmd_parser.add_option("-u", "--url", type="string", action="store", dest="solr_server_url", help="SOLR Server Status URL", metavar="http://server/stat/")
cmd_parser.add_option("-w", "--warning", type="float", action="store", dest="warning_per", help="Exit with WARNING status if higher than the PERCENT of CPU Usage", metavar="Warning Percentage")
cmd_parser.add_option("-c", "--critical", type="float", action="store", dest="critical_per", help="Exit with CRITICAL status if higher than the PERCENT of CPU Usage", metavar="Critical Percentage")
(cmd_options, cmd_args) = cmd_parser.parse_args()
# Check the Command syntax
if not (cmd_options.warning_per and cmd_options.critical_per and cmd_options.solr_server_url):
    cmd_parser.print_help()
    sys.exit(3)

# Collect Solr Statistics Object
class CollectStat:
    ''' Obejct to Collect the Statistics from the 'n'th Element of the XML Data'''
    def __init__(self,n):
        self.stats = {}
#        solr_all_stat = minidom.parse(urllib.urlopen(cmd_options.solr_server_url))
        solr_all_stat = minidom.parse('solr_stat.xml')
        for stat in solr_all_stat.getElementsByTagName('entry')[n].getElementsByTagName("stat"):
            self.stats[stat.getAttribute('name')] = stat.childNodes[0].data.strip()
# Check QPS
if cmd_options.qps :
    # Get the QPS Statistics
    solr_qps_stats = CollectStat(23)
    if float(solr_qps_stats.stats['avgRequestsPerSecond']) >= cmd_options.critical_per:
        print "SOLR QPS CRITICAL : %.2f requests per second | ReqPerSec=%.2freqs" % (float(solr_qps_stats.stats['avgRequestsPerSecond']), float(solr_qps_stats.stats['avgRequestsPerSecond']))
        sys.exit(2)
    elif float(solr_qps_stats.stats['avgRequestsPerSecond']) >= cmd_options.warning_per:
        print "SOLR QPS WARNING : %.2f requests per second | ReqPerSec=%.2freqs" % (float(solr_qps_stats.stats['avgRequestsPerSecond']), float(solr_qps_stats.stats['avgRequestsPerSecond']))
        sys.exit(1)
    else:
        print "SOLR QPS OK : %.2f requests per second | ReqPerSec=%.2freqs" % (float(solr_qps_stats.stats['avgRequestsPerSecond']), float(solr_qps_stats.stats['avgRequestsPerSecond']))
        sys.exit(0)
# Check Docs
elif cmd_options.doc :
    # Get the Documents Statistics
    solr_doc_stats = CollectStat(0)
    if int(solr_doc_stats.stats['numDocs']) >= int(cmd_options.critical_per):
        print "SOLR DOCS CRITICAL : %d Total Documents | numDocs=%d" % (int(solr_doc_stats.stats['numDocs']), int(solr_doc_stats.stats['numDocs']))
        sys.exit(2)
    elif int(solr_doc_stats.stats['numDocs']) >= int(cmd_options.warning_per):
        print "SOLR DOCS WARNING : %d Total Documents | numDocs=%d" % (int(solr_doc_stats.stats['numDocs']), int(solr_doc_stats.stats['numDocs']))
        sys.exit(1)
    else:
        print "SOLR DOCS OK : %d Total Documents | numDocs=%d" % (int(solr_doc_stats.stats['numDocs']), int(solr_doc_stats.stats['numDocs']))
        sys.exit(0)