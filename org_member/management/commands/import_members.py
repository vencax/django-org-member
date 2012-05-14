'''
Created on Dec 29, 2011

@author: vencax
'''
from django.core.management.base import BaseCommand
import csv
import logging
from django.contrib.auth.models import User
from org_member.models import OrgMember

import unicodedata
from django.db.transaction import commit_on_success

def make_username_string(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    uname = u''.join([c for c in nkfd_form if not unicodedata.combining(c)])
    uname = uname.replace(' ', '')
    return uname.lower()

class Command(BaseCommand):
    """
    Reads CSV file with following content:
    emailaddress;
    """
    args = ''
    help = 'Makes a new meal timetable for next N days'
    
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        spamReader = csv.reader(open(args[0], 'rb'), delimiter=',')
        try:
            headers = None
            for row in spamReader:
                if headers:
                    self.process_row(row, headers)
                else:
                    headers = self.readHeaders(row)
        except Exception, e:
            logging.error('Maybe UTF-16 file?? Convert to utf-8...')
            logging.exception(e)
            
    @commit_on_success
    def process_row(self, row, headers):
        username = self._extractVal('Nickname', row, headers).lower() or \
            make_username_string(self._extractVal('Family Name', row, headers)) or \
            make_username_string(self._extractVal('Given Name', row, headers))
            
        if not username:
            return
        
        logging.info('Processing: %s' % username)
        
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            u = User(username=username,
                     first_name=self._extractVal('Given Name', row, headers),
                     last_name=self._extractVal('Family Name', row, headers),
                     email=self._extractVal('E-mail 1 - Value', row, headers))
            u.save()
        
        if OrgMember.objects.filter(user__exact=u).exists():
            return
        phone = self._extractVal('Phone 1 - Value', row, headers) or None
        member = OrgMember(user=u,
                           desc=self._extractVal('Notes', row, headers)[:512],
                           place=self._extractVal('Address 1 - Formatted', row, headers),
                           typee=1,
                           tel=phone)
        member.save()
        
    def readHeaders(self, row):
        headers = {}
        cntr = 0
        for h in row:
            headers[h] = cntr
            cntr += 1
        return headers
    
    def _extractVal(self, key, row, headers):
        return row[headers[key]]