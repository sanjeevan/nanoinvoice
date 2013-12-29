#!/usr/bin/env python
import os
import optparse
import tempfile

from subprocess import Popen
from subprocess import PIPE

def wkhtml_bin():
    current_path = os.path.dirname(os.path.abspath(__file__))
    bin_path = os.path.abspath(os.path.join(current_path, '../bin'))
    return os.path.join(bin_path, 'wkhtmltopdf')

def wkhtml_to_pdf(url=''):
    """
    Convert a url to a pdf file, and return the path to the PDF on the local
    filesystem
    """
    
    # generate a temp filename for the pdf output file
    fd_id, output_file = tempfile.mkstemp('.pdf', prefix='invoice-export-')
    os.close(fd_id)

    command = '%s "%s" "%s" >> /tmp/wkhtp.log' % (wkhtml_bin(), url, output_file)
    print command
    try:
        p = Popen(command, shell=True, stderr=PIPE, close_fds=True)
        stdout, stderr = p.communicate()
        retcode = p.returncode

        if retcode == 0:
            return output_file
        else:
            print 'There was an error creating the PDF file'
            return False
    except OSError:
        return False

if __name__ == '__main__':
    filename = wkhtml_to_pdf('http://localhost:5000/invoice/pdf/3')
    print 'Saved to %s' % filename
