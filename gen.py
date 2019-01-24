import yaml, subprocess, sys
from drupalgen.functionality import functionality
from drupalgen.layout import layout
from drupalgen.theme import theme
import config

globalConf = config.globalConf
siteConf = config.siteConf

filename = sys.argv[1]

fh = open(filename, 'r')
ymlConf = yaml.load(fh.read())
fh.close()

if (not 'project_name' in ymlConf):
    exit(1)


if ('functionality' in ymlConf):
    try:
        funcObj = functionality(ymlConf['project_name'], globalConf, ymlConf['functionality'])
        funcObj.createMakeYaml()
        cmd = funcObj.getMakeCommand()
        print(cmd)
        subprocess.run(cmd.split())
        cmd = funcObj.getInstallCommand(siteConf['dbmasterlogin'], siteConf['dbmasterpwd'],
            siteConf['dbhost'], siteConf['dbprefix'], siteConf['dbpwd'])
        print(funcObj.getPrintInstallCommand())
        subprocess.run(cmd.split())
        cmd = funcObj.getAdminPwdCommand(siteConf['adminpwd'])
        #print(cmd)
        subprocess.run(cmd.split())
    except:
        print(sys.exc_info()[1])


if ('layout' in ymlConf):
    try:
        layoutObj = layout(ymlConf['project_name'], globalConf, ymlConf['layout'])
        for cmd in layoutObj.getBlockConfCommands():
            print(cmd)
            subprocess.run(cmd.split())
    except:
        print(sys.exc_info()[1])


if ('theme' in ymlConf):
    try:
        if (not 'theme' in ymlConf['theme']) and ('theme' in ymlConf['functionality']):
            ymlConf['theme']['theme'] = ymlConf['functionality']['theme']
        themeObj = theme(ymlConf['project_name'], globalConf, ymlConf['theme'])
        cmd = themeObj.getModuleEnableCommand()
        print(cmd)
        subprocess.run(cmd.split())
        cmd = themeObj.getColorCommand()
        print(cmd)
        subprocess.run(cmd.split(' ', maxsplit=5))
    except:
        print(sys.exc_info()[1])
