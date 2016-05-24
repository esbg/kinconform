#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
pdbs = form.getvalue('pdb_file')
email = form.getvalue('email')

def check_email_validity(email):
    # Check email validity - adopted from validate_email python package
    import re
    # All we are really doing is comparing the input string to one
    # gigantic regular expression.  But building that regexp, and
    # ensuring its correctness, is made much easier by assembling it
    # from the "tokens" defined by the RFC.  Each of these tokens is
    # tested in the accompanying unit test file.
    #
    # The section of RFC 2822 from which each pattern component is
    # derived is given in an accompanying comment.
    #
    # (To make things simple, every string below is given as 'raw',
    # even when it's not strictly necessary.  This way we don't forget
    # when it is necessary.)
    #
    WSP = r'[\s]'                                        # see 2.2.2. Structured Header Field Bodies
    CRLF = r'(?:\r\n)'                                   # see 2.2.3. Long Header Fields
    NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'        # see 3.2.1. Primitive Tokens
    QUOTED_PAIR = r'(?:\\.)'                             # see 3.2.2. Quoted characters
    FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
          WSP + r'+)'                                    # see 3.2.3. Folding white space and comments
    CTEXT = r'[' + NO_WS_CTL + \
            r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
    CCONTENT = r'(?:' + CTEXT + r'|' + \
               QUOTED_PAIR + r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
    # as well, but that would be circular.)
    COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
              r')*' + FWS + r'?\)'                       # see 3.2.3
    CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
           FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
    ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'           # see 3.2.4. Atom
    ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'      # see 3.2.4
    DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'   # see 3.2.4
    DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?' # see 3.2.4
    QTEXT = r'[' + NO_WS_CTL + \
            r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
    QCONTENT = r'(?:' + QTEXT + r'|' + \
               QUOTED_PAIR + r')'                        # see 3.2.5
    QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                    r'?' + QCONTENT + r')*' + FWS + \
                    r'?' + r'"' + CFWS + r'?'
    LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
                 QUOTED_STRING + r')'                    # see 3.4.1. Addr-spec specification
    DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
    DCONTENT = r'(?:' + DTEXT + r'|' + \
               QUOTED_PAIR + r')'                        # see 3.4.1
    DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                     r'(?:' + FWS + r'?' + DCONTENT + \
                     r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
    DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
             DOMAIN_LITERAL + r')'                       # see 3.4.1
    ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1

    # A valid address will match exactly the 3.4.1 addr-spec.
    VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'

    return re.match(VALID_ADDRESS_REGEXP, email) is not None

def fileToStr(infile):
    """Return a string contianing the contents of a file"""
    ihand = open(infile)
    contents = ihand.read()
    ihand.close()
    return contents

def main(pdbs, email):
    print fileToStr('template.html')
    if type(pdbs) == str:
        print pdbs
    else:
        for x in pdbs:
            print "%s</br>" % (x,)
    
    print "</html>"
    return

try:
    print "Content-type:text/html\r\n\r\n"
    main(pdbs, email)
except:
    cgi.print_exception()

