#!/usr/bin/python2
# vim: set fileencoding=utf-8 :
# Class to abstract some parts of the jiffybox API away
# API documentation: http://www.df.eu/fileadmin/media/doc/jiffybox-api-dokumentation.pdf
# Copyright (c) Alexander KÃb <nerkram@koeb.me>
# Licensed under the GNU General Public License version 3.
# http://www.gnu.org/licenses/gpl-3.0.html
# The actual Version of this module can be found here:
# https://github.com/akoeb/Jiffy


# TODO: 
# * error check
# * check return values
# * validate parameters
# * test test test
# * implemented only about half the commands but tested none!!

# the method calls contain all in the URL encoded values as own parameters, and in addition a dictionary that 
# contains parameters that are sent as payload on post or put requests


# HTTP connections with requests lib
import requests
#import json

# use an exception to throw validation errors:
class ValidationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



class Jiffy:


    ###################################################################
    def __init__(self, token, debug=False):
        "constructor: set up new API Object requires an  API token from domainfactory as param"

        self.protocol = "https"
        self.host = "api.jiffybox.de"
        if not token:
            raise Exception("You need an API token from domainfactory to use this module")
        self.token = token

        self.apiVersion = "v1.0"
        self.baseURL = "%s://%s/%s/%s" % (self.protocol, self.host, self.token, self.apiVersion)
        self.debugFlag = debug
        self.debug("Started Jiffy Object in DEBUG mode")

    ###################################################################
    def _get(self, param):
        "Helper method that abstracts get requests"

        url = "%s/%s" % (self.baseURL, param)

        self.debug("calling _get with url: %s" % url)

        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("Returned Status code was %s (expected 200) on url %s" % (r.status_code, url))

        # return json data as python dictionary:
        self.debug("response: %s" % r.json())

        return r.json()

    ###################################################################
    def _delete(self, param):
        "Helper method that abstracts delete requests"

        url = "%s/%s" % (self.baseURL, param)

        self.debug("calling _delete with url: %s" % url)

        r = requests.delete(url)
        if r.status_code != 200:
            raise Exception("Returned Status code was %s (expected 200) on url %s" % (r.status_code, url))

        # return json data as python dictionary:
        return r.json()

    ###################################################################
    def _post(self, param, payload):
        "Helper method that abstracts post requests"

        url = "%s/%s" % (self.baseURL, param)

        self.debug("calling _post with url: %s" % url)

        r = requests.post(url, payload)
        if r.status_code != 200:
            raise Exception("Returned Status code was %s (expected 200) on url %s" % (r.status_code, url))

        # return json data as python dictionary:
        return r.json()

    ###################################################################
    def _put(self, param, payload):
        "Helper method that abstracts put requests"

        url = "%s/%s" % (self.baseURL, param)

        self.debug("calling _put with url: %s" % url)


        r = requests.put(url, payload)
        if r.status_code != 200:
            raise Exception("Returned Status code was %s (expected 200) on url %s" % (r.status_code, url))

        # return json data as python dictionary:
        return r.json()

    ###################################################################
    def _validateParams(self, dictionary, required = ()):
        "Helper method to validate a dictionary with parameters: type and existance of required keys checked"
        if not type(dictionary) is dict:
            raise ValidationError("first param is not a dictionary: %s (%s)" % (type(dictionary), dictionary.to_s) )

        if not type(required) is tuple:
            raise ValidationError("second param is not a tuple: %s (%s)" % (type(tuple), required.to_s) )

        for item in required:
            if  not item in dictionary:
                raise ValidationError("Required Parameter %s not set in parameter dictionary (%s)" % (item, dictionary.to_s) )

        # now validate the parameters 
        for key in dictionary.keys():
            k = key.lower()
            if k in ('boxid','planid','backupid','dayid','timeid','ipid', 'targetid', 'checkid', 'checkinterval', 'reminderinterval', 'retrytolerance', 'contactgroups', 'port'):
                self._validateNumber(dictionary[key])
            #elif k == 'name':
            #    if len(dictionary[key]) > 30 or dictionary[key].matches("[^a-zA-Z0-9_()=!\*@.-]"):
            #        raise ValidationError("Name %s illegal" % dictionary[key])
            # TODO: continue here... 

    ###################################################################
    # validator for int:
    def _validateNumber(self, s):
        try:
            float(s)
        except ValueError:
            raise ValidationError("Variabls %s is not a number!" % s)


    ###################################################################
    def listAllBoxes(self):
        "List all Jiffy Boxes"
        return self._get("jiffyBoxes")

    ###################################################################
    def getBoxDetails(self, boxID):
        "List Jiffy Box Details"
        self._validateNumber(boxID)
        return self._get("jiffyBoxes/%s" % boxID)

    ###################################################################
    def deleteBox(self, boxID):
        "Delete a Jiffy Boxes"
        self._validateNumber(boxID)
        return self._delete("jiffyBoxes/%s" % boxID)

    ###################################################################
    def createBoxFromDistribution(self, params):
        "create a new Jiffy Box "
        self._validateParams(params, ('name','planid', 'distribution'))
        return self._post("jiffyBoxes", params)

    ###################################################################
    def createBoxFromBackup(self, params):
        "create a new Jiffy Box "
        self._validateParams(params, ('name','planid', 'backupid'))
        return self._post("jiffyBoxes", params)

    ###################################################################
    def changeBoxStatus(self, boxID, params):
        "change status of a box to either START, SHUTDOWN, PULLPLUG, FREEZE, THAW."
        self._validateParams(params, ('status',))
        return self._put("jiffyBoxes/%s" % boxID, params)

    ###################################################################
    def listAllBackups(self):
        "List all backups of all boxes"
        return self._get("backups")

    ###################################################################
    def listBackupsOneBox(self, boxID):
        "List all backups to one box"
        return self._get("backups/%s" % boxID)

    ###################################################################
    def activateBackup(self, boxID, params):
        "Activate a Backup on a Box"
        self._validateParams(params, ('dayid','timeid'))
        return self._post("backups/%s" % boxID, params)

    ###################################################################
    def changeBackup(self, boxID, params):
        "Change Settings of a Backup on a Box"
        self._validateParams(params, ('dayid','timeid'))
        return self._put("backups/%s" % boxID, params)


    ###################################################################
    def deactivateBackupsOneBox(self, boxID):
        "Deactivate backups on one box"
        return self._delete("backups/%s" % boxID)

    ###################################################################
    def deleteOneBackup(self, boxID, typeName, backupID):
        "Delete one backup"
        return self._delete("backups/%s/%s/%s" % (boxID, typeName, backupID ))

    ###################################################################
    def listAllPlans(self):
        "list all plans"
        return self._get("plans")

    ###################################################################
    def getPlanDetails(self, planID):
        "get details of one plan"
        return self._get("plans/%s" % planID)

    ###################################################################
    def listAllDistributions(self):
        "list all linux distributions"
        return self._get("distributions")

    ###################################################################
    def getDistributionDetails(self, distributionID):
        "get details of one linux distribution"
        return self._get("distributions/%s" % distributionID)


    ###################################################################
    def listAllIPs(self):
        "list all IP addresses"
        return self._get("ips")

    ###################################################################
    def getBoxIP(self, boxID):
        "get the IP addrress details of one box"
        return self._get("ips/%s" % boxID)

    ###################################################################
    def rerouteIPToOtherBox(self,sourceBoxID, ipID, params):
        "move an additional IP address from one box to the other"
        self._validateParams(params, ('targetid',))
        return self._put("/ips/%s/%s/move" % (sourceBoxID, ipID), payload)

    ###################################################################
    def listAllMonitors(self):
        "List all monitoring checks"
        return self._get("monitoring")

    ###################################################################
    def getMonitorDetails(self, checkID):
        "Show details of a monitoring check"
        return self._get("monitoring/%s" % checkID)

    ###################################################################
    def deleteMonitor(self, checkID):
        "Delete a monitoring check"
        return self._delete("monitoring/%s" % boxID)

    ###################################################################
    def createMonitor(self, params):
        "create a new monitoring check"
        self._validateParams(params, ('name', 'ip', 'checkType', 'port'))
        return self._post("monitoring", params)

    ###################################################################
    def duplicateMonitor(self, sourceCheckID, params):
        "duplicate a monitoring check with at least one changed parameter"
        self._validateParams(params, ('name', 'ip', 'checkType'))
        return self._post("monitoring/%s" % sourceCheckID, params)

    ###################################################################
    def getMonitorStatus(self, checkID):
        "Show status of a monitoring check"
        return self._get("monitoring/%s/status" % checkID)

    ###################################################################
    def getAllMonitoringStatusesOfOneIP(self, IP):
        "Show status of all monitoring checks on one IP address"
        return self._get("monitoring/%s/status" % IP)

    ###################################################################
    def listAllContactGroups(self):
        "List all contact groups"
        return self._get("contactGroups")

    ###################################################################
    def getContactGroupDetails(self, groupID):
        "Show details of a contact group"
        return self._get("contactGroup/%s" % groupID)

    ###################################################################
    def deleteContactGroup(self, groupID):
        "Delete a contact group"
        return self._delete("contactGroup/%s" % groupID)

    ###################################################################
    def createContactGroup(self, params):
        "create a new contact group"
        self._validateParams(params, ('name', 'contacts'))
        return self._post("contactGroup", params)

    ###################################################################
    def changeContactGroup(self, params):
        "change an existing contact group"
        self._validateParams(params, ('name', 'contacts'))
        return self._put("contactGroup", params)

    ###################################################################
    def duplicateContactGroup(self, sourceID, params):
        "duplicate an existing contact group"
        self._validateParams(params, ('name', 'contacts'))
        return self._post("contactGroup/%s" % sourceID, params)

    ###################################################################
    def listAllDocumentationModules(self):
        "List all documentation modules"
        return self._get("doc")

    ###################################################################
    def getContactGroupDetails(self, docModule):
        "Show details of one documentation module"
        return self._get("doc/%s" % docModule)


    ###################################################################
    def debug(self, msg):
        if self.debugFlag:
            print msg


