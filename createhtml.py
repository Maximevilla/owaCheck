import datetime
import os
import imgkit
from jinja2 import Environment, FileSystemLoader
import glob

def createhtml(searchpasswords,search,template_vars,users,datescantime):

    searchfolders = []
    if searchpasswords == 'True':
        searchfolders.append('password')
    if search != '':
        searchfolders.append(search)
    template_vars["searchfolders"]=searchfolders


    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template.html")

    cwd = os.path.dirname(os.path.abspath(__file__))
   # datescan = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
    newpath = r'.\\'+str(datescantime)

    ## Creates datefolder
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    ## Add to template_env the dateNameFolder
    template_vars['folderdate'] = datescantime


    # Creates report per user
    for user in users:
        print(template_vars)
        jpgfiles = []
        template_vars[user] = {}
        print(template_vars)
        template_vars['current'] = user
        template_vars['users'][user]["PasswordsInMails"] = []
        template_vars['users'][user][search] = []

        pages = glob.glob(cwd+'\\' + str(datescantime) +'\\'+ user + '\\' + '**/*.html')   ## Searchs webpages in folder

        # Creates JPG for each webpage
        for index in range(len(pages)):
            try:
                jpgfile = pages[index] + '.jpg'
                imgkit.from_file(pages[index], jpgfile)
                jpgfiles.append(jpgfile)
                print(pages[index])
            except:
                pass

        # Creates webpage per working username

        if any("password" in s for s in pages):
            for s in pages:
                if "password".lower() in s.lower():
                    template_vars['users'][user]["PasswordsInMails"].append(s)


        if any(search in s for s in pages):
            for s in pages:
                if search.lower() in s.lower():

                    template_vars['users'][user][search].append(s)


        template_vars['thumbs']=jpgfiles
        template_vars['pages'] = pages

        template_vars['cwd'] = cwd
        template = env.get_template("template.html")
        html_out = template.render(template_vars)
        with open(r'.\\' + str(datescantime) + '\\' + user + '.html', 'a') as html_file:
            html_file.write(html_out)


    #Creates Summary
    template = env.get_template("report_template.html")
    html_out = template.render(template_vars)

    with open(r'.\\' + str(datescantime) + '\\' + 'report' + '.html', 'a') as html_file:
        html_file.write(html_out)

