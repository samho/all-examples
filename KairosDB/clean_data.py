#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
import optparse
import datetime

KAIROSDB_URL = "http://123.207.92.112:8080"
KAIROSDB_USER = "gizwits"
KAIROSDB_PWD = "go4gizwits"


def get_metrics_list():
    auth = HTTPBasicAuth(KAIROSDB_USER, KAIROSDB_PWD)
    url = "%(main_url)s/api/v1/metricnames" % ({"main_url": KAIROSDB_URL})
    #print url
    r = requests.get(url=url, auth=auth)
    content = r.json()
    #for metric in content["results"]:
    #    print metric
    return content["results"]


def get_metric_value(metric_payload):
    auth = HTTPBasicAuth(KAIROSDB_USER, KAIROSDB_PWD)
    payload = metric_payload
    url = "%(main_url)s/api/v1/datapoints/query" % ({"main_url": KAIROSDB_URL})
    r = requests.post(url, data=json.dumps(payload), auth=auth)
    content = r.json()
    #print "Content:", content["queries"][0]["results"][0]["values"]
    return content["queries"][0]["results"][0]["values"]


def delete_metrics_with_date_range(start, end, metricname, noinput):
    print "====== Start to delete ======"
    print "------ ", datetime.datetime.now(), " ------"
    auth = HTTPBasicAuth(KAIROSDB_USER, KAIROSDB_PWD)
    del_url = url = "%(main_url)s/api/v1/datapoints/delete" % ({"main_url": KAIROSDB_URL})
    metricname_list = []
    if metricname == "all":
        metricname_list = get_metrics_list()
    else:
        metricname_list.append(metricname)

    for metric in metricname_list:
        metric_payload = {
            "metrics": [
                {
                    "tags": {},
                    "name": "%(metrics_name)s" % ({"metrics_name": metric})
                }
            ],
            "cache_time": 0,
            "start_absolute": start,
            "end_absolute": end
        }
        metric_value = get_metric_value(metric_payload)
        print "Metric Name: ", metric
        print "Metric Value is:", metric_value
        if noinput:
            print "All metric between %s and %s will been deleted." % (start, end)
            print "######"
            r = requests.post(del_url, data=json.dumps(metric_payload), auth=auth)
            if r.status_code == 204:
                print "[%s] has been deleted successfully." % metric
            else:
                print "[%s] cannot be deleted, the response code is %d" % (metric, r.status_code)
                print "######\n"
        else:
            confirm = raw_input("Confirmation: Are you sure to delete the metric name [%s] (y/n): " % metric)
            if confirm == 'y':
                r = requests.post(del_url, data=json.dumps(metric_payload), auth=auth)
                if r.status_code == 204:
                    print "[%s] has been deleted successfully." % metric
                else:
                    print "[%s] cannot be deleted, the response code is %d" % (metric, r.status_code)
            else:
                print "[%s] will be ignored, continue to next one." % metric
                continue

    print "====== All have been done. ======"
    print "------ ", datetime.datetime.now(), " ------"


if __name__ == "__main__":
    p = optparse.OptionParser()

    p.add_option("-s", "--start", action="store", dest="startdate", type="long", help="Start date.")
    p.add_option("-e", "--end", action="store", dest="enddate", type="long", help="End date.")
    p.add_option("-m", "--metric", action="store", dest="metricname", type="string", help="Metric name for deleted.")
    p.add_option("-n", "--no-input", action="store_true", default=False, dest="noinput", help="Delete without confirm.")

    p.set_defaults(metricname="all")

    opt, args = p.parse_args()

    print "start: ", opt.startdate
    print "end: ", opt.enddate
    print "metric name: ", opt.metricname
    print "no-input", opt.noinput

    delete_metrics_with_date_range(opt.startdate, opt.enddate, opt.metricname, opt.noinput)
    #metric_list = get_metrics_list()
    #get_metric_value(opt.metricname, opt.startdate, opt.enddate)



