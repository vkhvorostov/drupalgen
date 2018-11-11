from pathlib import Path

class layout:


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


    def getBlockConfCommands(self):
        result = list()
        for region in self.conf['regions']:
            cmdStart = self.drushPath + ' -r ' + self.projectPath + ' block-configure' + ' --region=' + region
            for block in self.conf['regions'][region]:
                (module, delta) = block.split('_')
                cmd = cmdStart + ' --module=' + module + ' --delta=' + delta
                if (block in self.conf['blocks']):
                    cmd = cmd + ' --weight=' + str(self.conf['blocks'][block])
                    result.append(cmd)
        return result