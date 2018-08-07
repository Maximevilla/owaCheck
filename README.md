# owaCheck
SimpleScript to check from a file with username:password 

~~~~
$ python mailcheck.py --help                                                
Usage: mailcheck.py [OPTIONS]                                               
                                                                            
Options:                                                                    
  --checkpasswords TEXT  If True checks for password in this mailbox and    
                         retrieves mails                                    
  --out TEXT             Output fileName                                    
  --server TEXT          IMAP server address                                
  --file TEXT            Input fileName. Format : "mail:password"           
  --help                 Show this message and exit.                        
                                                                            
~~~~
**works on IMAP**

The default output is afile named out.txt

Do a second round checking for each valid email account for the word password in it

> TODO :: Enhance option --checkpassword
>
