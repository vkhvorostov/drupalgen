from pathlib import Path
import json

class theme:


    conf = {}
    projectName = ''
    drushPath = ''
    projectPath = ''


    def __init__(self, projectName, globalConf, conf):
        if (not isinstance(projectName, str) or len(projectName) == 0):
            raise ValueError("projectName must be not empty string")
        #print(conf)
        self.projectName = projectName
        self.drushPath = globalConf['drushPath']
        self.projectPath = globalConf['projectsPath'] + self.projectName
        self.conf = conf
        pFile = Path(self.projectPath)
        if (not pFile.exists()):
            raise ValueError("project dir not exists")


    def getColorCommand(self):
        return self.drushPath + ' -r ' + self.projectPath + ' stc ' + self.conf['theme'] \
            + " " + json.dumps(self.conf['palette'])


    def getModuleEnableCommand(self):
        return self.drushPath + ' -y -r ' + self.projectPath + ' en subtheme_color'


