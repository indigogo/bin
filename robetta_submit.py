#! /usr/bin/env python
#
# Submits a sequence for modeling on Robetta.
# Requires a Robetta account with "Full Prediction" enabled.
from argparse import ArgumentParser
from os.path import exists
from urllib import urlencode, urlopen
from util import read_fasta
import re

server_address = 'http://www.robetta.org/cgi-bin/submit.cgi'

def build_request(options):
    '''Constructs an HTTP request from the specified options'''
    params = { "Email": "%email%", "Sequence": "%sequence%", "Method":"0", "ReplyEmail":"%email%", "Notes": "%title%" }
    params['Email'] = options['registered_email']
    params['ReplyEmail'] = options['reply_email']
    params['Sequence'] = options['sequence']    
    params['Notes'] = options['name']
    return urlencode(params)


def validate_sequence(sequence):
    '''Raises ValueError if input sequence is invalid'''
    if not re.match('^[A-Z]+$', sequence):
        raise ValueError('Invalid protein sequence')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--registered_email', required = True, help = 'Robetta registered email address')
    parser.add_argument('--reply_email', required = True, help = 'Email address to send results')
    parser.add_argument('--sequence', help = 'Protein sequence to model')
    parser.add_argument('--fasta', help = 'FASTA file containing protein sequence to model')
    parser.add_argument('--name', required = True, help = 'Identifier for this job')
    options = vars(parser.parse_args())

    # Ensure that --fasta or --sequence was provided, but not both
    has_fasta = options['fasta']
    has_sequence = options['sequence']
    provided_none = not(has_fasta or has_sequence)
    provided_many = has_fasta and has_sequence

    if provided_none or provided_many:
        print 'Must provide either --fasta or --sequence'
        exit(1)

    # Read sequence from file
    if has_fasta:
        filename = options['fasta']
        if not exists(filename):
            print 'Unable to read FASTA => %s' % filename
            exit(1)

        header, options['sequence'] = read_fasta(filename)

    try:
        validate_sequence(options['sequence'])
        request = build_request(options)
        response = urlopen(server_address, request)
        print response.read()
    except Exception, e:
        print 'Submission failed:', e
