# owaCheck
SimpleScript to check from a file with username:password if they are valid on a mailServer. The name just comes from my first usage

~~~~
$ python mailcheck.py --help                                                
Usage: mailcheck.py [OPTIONS]

Options:
  --html TEXT             If True generates an html report. Works only if
                          --search or --searchpassword used
  --search TEXT           [OPTIONAL] Search in this mailbox and retrieves mails
                          with this word
  --searchpasswords TEXT  [OPTIONAL] If True checks for password in this mailbox
                          and retrieves mails
  --out TEXT              [OPTIONAL] default:out.txt Output fileName 
  --server TEXT           IMAP server address
  --file TEXT             Input fileName. Format : "mail:password"
  --help                  Show this message and exit.                                                                                           
~~~~

**works on IMAP**

The default output is a file named out.txt

Do a second round checking for each valid email account for the word password in it with --passwordsearch True
Generate an html report with thumbnails for easy search with --html True

**Install**

You will need to install wkhtmltoimage from https://wkhtmltopdf.org/downloads.html

Then run :

~~~~
got clone https://github.com/Maximevilla/owaCheck
cd owaCheck
python setup.py install
~~~~

TODO : 
* password spray
* List of known Imap server for domains in order to make Mixed domains search easyier
