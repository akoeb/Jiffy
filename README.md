# Jiffy  

Python module that implements the JiffyBox API

## Description

JiffyBox is a cloud system from domainfactory GmbH, details can be found under http://www.df.eu/de/cloud-hosting/cloud-server/ (German)
This python module implements the API from JiffyBox as documented under http://www.df.eu/fileadmin/media/doc/jiffybox-api-dokumentation.pdf

Many of the API calls are implemented without being tested, I basically typed down the API as it is documented and tested only the functions that I needed myself. So if you find any error, I would be happy if you send me a bug report or even better a pull request with the bugfix.

Additionally, if you want to give me any hints or comments about coding style, best practices or your local beer preferences, I am happy to hear about it.

Also you can send me feature requests, but I don't promise to implement them, that depends on my time and my mood. However, you could consider hiring me if you have urgent feature requests ;-)


## Usage Example

```python

# import the module:
from Jiffy import Jiffy

# create jiffy object
jiffy = Jiffy("<YOUR JIFFYBOX TOKEN>", False)

#
#
# get an object that contains all information about all boxes:    
allBoxes = jiffy.listAllBoxes()

# show only Status and BoxID
for boxID in allBoxes['result'].keys():
    print "boxID: %s, Status: %s" % (boxID, allBoxes['result'][boxID]['status'])

    # get the details object for one box:
    print jiffy.getBoxDetails(boxID)

    # shut down the box
    jiffy.changeBoxStatus(boxID, {"status": "SHUTDOWN"})

#
# 
# create a box with following parameters:
createParams = { "planid": planid,
    "distribution": "debian_wheezy_64bit",
    "name": boxName,
    "password":"SUPER-SECURE-ROOT-PASSWORD",
    "use_ssh_key":0,
    "metadata": {} }

# this creates the box:
result = jiffy.createBoxFromDistribution(createParams)
if not result['result']:
    sys.exit("Error while creating VM: %s" % result['messages'][0]['message'])

# read box data and included box id from result:
newBox = result['result']
newBoxID = newBox['id']


# box creation takes a couple of minutes to be finished, poll for status 'READY'.
# warning: this code does NOT implement a timeout!
while (True):
    result = jiffy.getBoxDetails(newBox['id'])['result']
    if result['status'] == 'READY':
        # to avoid race conditions, wait another 2 secs
        sleep(2)
        print "Box %s, id %s, IP %s, status READY." % (boxName, result['id'], result['ips']['public'][0])
        break
    # poll every 10 secs
    sleep(10)





```

There are many more api calls implemented, some of them are not even tested very thoroughly. Read the source, Luke!


## Requirements

The module uses the python-requests library to make the actual calls.

## TODO

Actually a lot, the module is an a state so I can use it, but a lot is still missing for global usage. an incomplete list:
* Error checking, basically no error checks are implemented yet
* check of return values
* validate input parameters, I just began with that
* test
* test
* test

## License

GPLv3 - see LICENSE file for full license statement

## Author

Alexander Köb< nerdkram@koeb.me>
