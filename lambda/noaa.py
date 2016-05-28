import urllib
import urllib2
import re
import copy

from xml.dom import minidom
from time import strftime,strptime

class Noaa(object):

    ENDPOINT = 'http://forecast.weather.gov/product.php'

    SECTIONS = ['SYNOPSIS', 'DISCUSSION']

    
    DICT = {
        'kt': 'knots',
        r'\bNAM\b': 'model',
        r'\b([0-9]+)Z\b': r'\1' + " o'clock",
        r'\n': ' ',
        r'&&': '',
        r'\.\.\.': ': '         # handle pauses correctly
        }

    TRANSLATIONS = {re.compile(regx) : replacement for (regx,replacement) in DICT.iteritems()}

    def __init__(self):
        self.raw_body = ''
        self.sections = {
            'SYNOPSIS': 'Could not extract synopsis',
            'DISCUSSION': 'Could not extract discussion'
        }
        self.error = None

    def get_afd_for(self,station_name):
        self.get_raw_afd(station_name)
        self.parse_body()
        self.subst_body()

    def get_raw_afd(self,station_name):
        """
        Get raw HTML feed with minimal decoration into self.raw_body. 
        There doesn't seem to be an XML or JSON version available.
        """
        params = {
            'site': 'NWS',
            'product': 'AFD',
            'issuedby': station_name,
            'format': 'txt',
            'version': '1'
        }
        url = '{}?{}'.format(self.ENDPOINT, urllib.urlencode(params))
        try:
            self.raw_body = urllib2.urlopen(url).read()
        except urllib2.URLError:
            self.error = 'The NOAA website did not respond.'


    def parse_body(self):
        """
        Parse the raw_body into sections.  Section name FOO seems to be
        delimited by regex ^\s*.FOO\.\.\.  so split on that regex and
        discard the first piece, which precedes .SYNOPSIS...
        """
        match = re.compile('.*^\.SYNOPSIS\.\.\.(.*)^\.DISCUSSION', re.MULTILINE|re.DOTALL).match(self.raw_body)
        if match:
            self.sections['SYNOPSIS'] = match.group(1)

        match = re.compile('.*^\.DISCUSSION\.\.\.(.*)^\.AVIATION', re.MULTILINE|re.DOTALL).match(self.raw_body)
        if match:
            self.sections['DISCUSSION'] = match.group(1)

    def subst_body(self):
        """
        In each chunk of text, do substitutions against a built-in dictionary
        so that Alexa will correctly speak certain jargon and abbreviations.
        """
        for section_name in self.sections:
            for regex,replacement in Noaa.TRANSLATIONS.items():
                text = self.sections[section_name]
                new_str = re.sub(regex,replacement,text)
                self.sections[section_name] = new_str
