import os
import cvtest2

class ImageFolder():
    def __init__(self, loc):
        if not loc.endswith('/'):
            loc += ('/')
        foldername = str(loc.split('/')[-2])
        print 'foldername: ', foldername, ' loc: ', loc
        self.ra = foldername.split('_')[0]
        self.note = foldername.split('_')[1]
        self.data = []
        os.chdir(loc)

        filenames = os.walk('.').next()[2]
        for filename in filenames:
            if loc.endswith('/'):
                self.data.append( cvtest2.analyze_file(loc + filename))
            else:
                self.data.append(cvtest2.analyze_file(loc + '/' + filename))

    def __repr__(self):
        return 'imagefolder with name: ' + \
               str(self.note) + \
               ', ra:' + \
                str(self.ra) + \
               '\nvar: ' + \
               str(self.data)





