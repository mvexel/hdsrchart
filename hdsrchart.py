import matplotlib as mpl
mpl.use('Agg') # to use MatPlotLib without an X server
import matplotlib.pyplot as plt
from matplotlib import dates
import urllib
import urllib2
import os
import simplejson as json
from datetime import datetime, date

# hdsrchart.py
# ============
#
# this hack was done for Hack De Overheid to demonstrate a simple user
# case for the HDSR API.
#
# License
# =======
# Copyright (c) 2012 Martijn van Exel
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# CONFIGURATION
# ======================================================================
# outdir - change to wherever you want the chart saved
outdir = '/home/mvexel/tmp/'
# startdate - change to desired start date
startdate = date(2012,3,31)
# enddate - change to desired end date
enddate = date(2012,4,7)
# baseurl - this is just an example, see http://hdsrapi.lizard.net/ 
# for more 
baseurl = 'http://hdsrapi.lizard.net/o_watergang(pd)/HGTE_METING_15M/'
# watergang_id - this is just an example, see http://hdsrapi.lizard.net/ 
# for more 
watergang_id = '001-w_Bermsloot Romeinenbaan west_ben'
# ======================================================================

# we want the data back as json
suffix = '?format=json&start=%s&end=%s' % (startdate.isoformat(), enddate.isoformat())
# build the API url
api_url = baseurl + urllib.quote(watergang_id + '/' + suffix)

# get the data
responseobj = urllib2.urlopen(api_url)
metingen = json.loads(responseobj.read())

# initialize X and Y axis data lists
dts = []
hoogtes = []
# iterate over json object storing data
for meting in metingen:
    if meting['time'] and meting['value']:
        dts.append(datetime.strptime(meting['time'],'%Y-%m-%d %H:%M:%S'))
        hoogtes.append(meting['value'])

minh = min(hoogtes)
maxh = max(hoogtes)

# MATPLOTLIB initialization stuff
# ======================================================================
# initialize 8x6 figure object
fig = plt.figure(figsize=(8,6))
# set font
font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 9}
mpl.rc('font', **font)
# initialize formatter for dates on X axis
hfmt = dates.DateFormatter('%d-%m-%Y %H uur')
# define axes
ax = fig.add_subplot(111,autoscale_on=False, xlim=(startdate, enddate), ylim=(minh, maxh))
ax.xaxis.set_major_formatter(hfmt)
locator = dates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
# set axis labels
plt.ylabel('Waterhoogte')
plt.xlabel('Datum')
# set chart title
plt.title('Waterhoogte ' + watergang_id)
# rotate x labels to make it fit nicer
fig.autofmt_xdate(rotation=45)
# ======================================================================


# define the chart line with the x and y value lists
line = ax.plot(dts,hoogtes)
# set line thickness to 3
plt.setp(line, linewidth=3.0)

# save the chart to the file system
outpath = os.path.join(outdir, watergang_id.replace(' ','_') + '.png')
fig.savefig(outpath, dpi=96)

print 'done. chart saved as %s' % (outpath)
