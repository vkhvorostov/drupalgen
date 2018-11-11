import yaml
from pathlib import Path

class functionality:


    conf = {}
    projectName = ''
    makeFileName = ''
    drushPath = ''
    projectPath = ''
    makeDefaults = {
        'core': '7.x',
        'api': '2',
        'projects': {
            'drupal': {'version': None}
        },
        'translations': ['ru']
    }


    def __init__(self, projectName, globalConf, conf):
        if (not isinstance(projectName, str) or len(projectName) == 0):
            raise ValueError("projectName must be not empty string")
        #print(conf)
        self.projectName = projectName
        self.drushPath = globalConf['drushPath']
        self.projectPath = globalConf['projectsPath'] + self.projectName
        self.makeFileName = 'make_' + self.projectName + '.yml'
        self.conf = conf
        pFile = Path(self.projectPath)
        if (pFile.exists()):
            raise ValueError("project dir already exists")


    def createMakeYaml(self):

        components = list()
        if ('tasks' in self.conf):
            for task in self.conf['tasks']:
                if ('component' in task):
                    components.append(task['component'])

        make = self.makeDefaults
        for component in components:
            if (component in self.conf['component_configuration']):
                make['projects'][component] = self.conf['component_configuration'][component]
            else:
                make['projects'][component] = {'version': None}

        fh = open(self.makeFileName, 'w')
        yaml.dump(make, fh)
        fh.close()


    def getMakeCommand(self):
        return self.drushPath + ' make ' + self.makeFileName + ' ' + self.projectPath


    def getInstallCommand(self, login, pwd, dbmasterlogin, dbmasterpwd, dbhost, dbprefix, dbpwd):
        return self.drushPath + ' si standard -r ' + self.projectPath \
               + ' --account-name ' + login + ' --account-pass ' + pwd \
               + ' --db-su=' + dbmasterlogin + ' --db-su-pw=' + dbmasterpwd \
               + ' --db-url=mysql://' + dbprefix + '_' + self.projectName + ':' + dbpwd + '@' + dbhost \
               + '/' + dbprefix + '_' + self.projectName + ' --site-name=' \
               + self.projectName + ' --locale=ru'
