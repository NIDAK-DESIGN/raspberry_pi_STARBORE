class cLanguage:

    def __init__(self):
        
        with open("cfg.txt") as f:
            contents = f.readlines()
            f.close()

        for line in contents:
            if "lang:" in line:
                self.langIdx = int(line.split(":")[1])


        with open("lang.txt") as f:
            contents = f.readlines()
            f.close()

        self.texts = {}
        for line in contents:
            #print(line)
            fields = line.split(";")
            if len(fields) > self.langIdx:
                self.texts[fields[0]] = fields[self.langIdx]
            else:
                self.texts[fields[0]] = fields[ 0 ]

        #print(self.texts)

    def tr(self, txt):
        return self.texts[txt]
            
        
