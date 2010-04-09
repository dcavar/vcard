#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test suite for vcard module

Default syntax:

./vcard_test.py
    Run all unit tests
"""
import unittest
import warnings

import vcard

# pylint: disable-msg=C0301
# Invalid vCards
VCARD_EMPTY = ''
VCARDS_MISSING = {
    'properties': 'BEGIN:VCARD\r\nEND:VCARD\r\n',
    'start': 'VERSION:3.0\r\nN:Doe;John;Ottoman;Mr;\r\nFN:John Ottoman Doe\r\nEND:VCARD\r\n',
    'end': 'BEGIN:VCARD\r\nVERSION:3.0\r\nN:Doe;John;Ottoman;Mr;\r\nFN:John Ottoman Doe\r\n',
    'version': 'BEGIN:VCARD\r\nN:Doe;John;Ottoman;Mr;Jr\r\nFN:John Ottoman Doe\r\nEND:VCARD\r\n',
    'n': 'BEGIN:VCARD\r\nVERSION:3.0\r\nFN:John Doe\r\nEND:VCARD\r\n',
    'fn': 'BEGIN:VCARD\r\nVERSION:3.0\r\nN:Doe;John;;Mr;\r\nEND:VCARD\r\n'}
VCARDS_INVALID_PROPERTY_NAME = {
    'foobar': 'BEGIN:VCARD\r\nVERSION:3.0\r\nFOO:bar\r\nN:Doe;John;;Mr;\r\nFN:John Doe\r\nEND:VCARD\r\n'}
VCARDS_INVALID_PARAM = {
    }
VCARDS_INVALID_PARAM_VALUE = {
    }
VCARDS_INVALID_VALUE = {
    'http://en.wikipedia.org/wiki/VCard': u"""BEGIN:VCARD\r\nVERSION:3.0\r\nN:Gump;Forrest\r\nFN:Forrest Gump\r\nORG:Bubba Gump Shrimp Co.\r\nTITLE:Shrimp Man\r\nTEL;TYPE=WORK,VOICE:(111) 555-1212\r\nTEL;TYPE=HOME,VOICE:(404) 555-1212\r\nADR;TYPE=WORK:;;100 Waters Edge;Baytown;LA;30314;United States of America\r\nLABEL;TYPE=WORK:100 Waters Edge\\nBaytown, LA 30314\\nUnited States of America\r\nADR;TYPE=HOME:;;42 Plantation St.;Baytown;LA;30314;United States of America\r\nLABEL;TYPE=HOME:42 Plantation St.\\nBaytown, LA 30314\\nUnited States of America\r\nEMAIL;TYPE=PREF,INTERNET:forrestgump@example.com\r\nREV:20080424T195243Z\r\nEND:VCARD\r\n""",
    'http://microformats.org/tests/hcard/01-tantek-basic.vcf': u"""BEGIN:VCARD\r\nFN;CHARSET=UTF-8:Tantek Çelik\r\nN;CHARSET=UTF-8:Çelik;Tantek;;;\r\nNAME:01-tantek-basic\r\nORG;CHARSET=UTF-8:Technorati\r\nPRODID:$PRODID$\r\nSOURCE:http://microformats.org/test/hcard/01-tantek-basic.html\r\nURL:http://tantek.com/\r\nVERSION:3.0\r\nEND:VCARD\r\n""",
    }

# Valid vCards
VCARDS_VALID = {
    'minimal': 'BEGIN:VCARD\r\nVERSION:3.0\r\nN:Doe;John;;Mr;\r\nFN:John Doe\r\nEND:VCARD\r\n',
    'scrambled_case': 'bEGIn:VCaRD\r\nVErsiON:3.0\r\nn:Doe;John;;Mr;\r\nfN:John Doe\r\nEnD:vcArD\r\n',
    'http://aspaass.no/kontakt/Aspaas%20Sykler.vcf': u"""BEGIN:VCARD\r\nVERSION:3.0\r\nPROFILE:VCARD\r\nCLASS:PUBLIC\r\nSOURCE:http\\://aspaass.no/Aspaas Sykler.vcf\r\nN:Aspaas Sykler;;;;\r\nFN:Aspaas Sykler\r\nORG:Aspaas Sykler\r\nURL;TYPE=WORK:http\\://aspaass.no/\r\nEMAIL;TYPE=INTERNET;TYPE=PREF;TYPE=WORK:aspaass@online.no\r\nTEL;TYPE=VOICE;TYPE=PREF;TYPE=MSG;TYPE=WORK:+4733187525\r\nTEL;TYPE=FAX;TYPE=WORK:+4733183703\r\nADR:;;Nansetgata 74;Larvik;Vestfold;3269;Norway\r\nLABEL:Nansetgata 74\\n3269 Larvik\\nNorway\r\nPHOTO;VALUE=uri:http\\://aspaass.no/include/image/butikk.jpg\r\nNOTE:Åpningstider mandag til fredag 9-18; lørdag 9-16\r\nTZ:+01\\:00\r\nGEO:59.06116,10.03712\r\nLOGO;VALUE=uri:http\\://aspaass.no/include/image/logo.png\r\nCATEGORIES:business,Norwegian\r\nEND:VCARD\r\n""",
    'http://www.troywolf.com/articles/php/class_vcard/vcard_example.php': """BEGIN:VCARD\r\nVERSION:3.0\r\nCLASS:PUBLIC\r\nPRODID:-//class_vcard from TroyWolf.com//NONSGML Version 1//EN\r\nREV:2010-03-17 09:36:59\r\nFN:Troy Wolf\r\nN:Wolf;Troy;;;\r\nNICKNAME:TJ\r\nTITLE:Web Developer\r\nORG:TroyWolf.com\r\nADR;TYPE=work:;;7027 N. Hickory;Kansas City;MO;64118;\r\nADR;TYPE=home:;;7027 N. Hickory;Kansas City;MO;64118;\r\nEMAIL;TYPE=internet,pref:troy@troywolf.com\r\nTEL;TYPE=cell,voice:(816) 739-9653\r\nURL;TYPE=work:http://www.troywolf.com\r\nBDAY:1971-08-13\r\nTZ:-06:00\r\nEND:VCARD\r\n""",
    }

VCARDS_REFERENCE = {
    'http://tools.ietf.org/html/rfc2426 1': u"""BEGIN:vCard\r\nVERSION:3.0\r\nFN:Frank Dawson\r\nORG:Lotus Development Corporation\r\nADR;TYPE=WORK,POSTAL,PARCEL:;;6544 Battleford Drive\r\n ;Raleigh;NC;27613-3502;U.S.A.\r\nTEL;TYPE=VOICE,MSG,WORK:+1-919-676-9515\r\nTEL;TYPE=FAX,WORK:+1-919-676-9564\r\nEMAIL;TYPE=INTERNET,PREF:Frank_Dawson@Lotus.com\r\nEMAIL;TYPE=INTERNET:fdawson@earthlink.net\r\nURL:http://home.earthlink.net/~fdawson\r\nEND:vCard\r\n""",
    'http://tools.ietf.org/html/rfc2426 2': u"""BEGIN:vCard\r\nVERSION:3.0\r\nFN:Tim Howes\r\nORG:Netscape Communications Corp.\r\nADR;TYPE=WORK:;;501 E. Middlefield Rd.;Mountain View;\r\n CA; 94043;U.S.A.\r\nTEL;TYPE=VOICE,MSG,WORK:+1-415-937-3419\r\nTEL;TYPE=FAX,WORK:+1-415-528-4164\r\nEMAIL;TYPE=INTERNET:howes@netscape.com\r\nEND:vCard\r\n"""}

# pylint: enable-msg=C0301

class TestVCards(unittest.TestCase):
    """Test small vCards"""
    def test_empty(self):
        """Empty string"""
        try:
            vcard.VCard(VCARD_EMPTY)
            self.fail('Invalid vCard created')
        except vcard.VCardFormatError as error:
            self.assertEquals(error.message, vcard.MSG_EMPTY_VCARD)

    def test_missing(self):
        """vCards missing a mandatory property"""
        for vcard_title, vcard_text in VCARDS_MISSING.items():
            try:
                vcard.VCard(vcard_text)
                self.fail('Invalid vCard "%s" created' % vcard_title)
            except vcard.VCardFormatError as error:
                self.assertEquals(
                    error.message[:len(vcard.MSG_MISSING_PROPERTY)],
                    vcard.MSG_MISSING_PROPERTY)

    def test_valid(self):
        """Valid (but not necessarily sane) vCards"""
        for vcard_title, vcard_text in VCARDS_VALID.items():
            try:
                with warnings.catch_warnings(record=True):
                    vc_obj = vcard.VCard(vcard_text)
                self.assertNotEqual(vc_obj, None)
            except vcard.VCardFormatError as error:
                self.fail(
                    'Valid vCard "%s" not created' % vcard_title + '\n' + \
                    error.message)

    def test_rfc_2426_examples(self):
        """
        Examples from RFC 2426 <http://tools.ietf.org/html/rfc2426#section-7>
        Skipping because RFC vCards are not valid :/
        <http://l0b0.wordpress.com/2009/12/25/vcard-parser-and-validator/>
        """
        for vcard_text in VCARDS_REFERENCE.values():
            try:
                with warnings.catch_warnings(record=True):
                    vc_obj = vcard.VCard(vcard_text)
                self.assertNotEqual(vc_obj, None)
            except vcard.VCardFormatError:
                pass
                #self.fail(
                #    'Valid vCard "%s" not created' % vcard_title + '\n' + \
                #    error.message)

def main():
    """Command line options checkpoint"""
    unittest.main()

if __name__ == '__main__':
    main()