from matplotlib import pyplot as plt

class BandiRecorder(object):
    def __init__(self):
        self.x, self.y = [], []
        self.ref_x, self.ref_y = [], []

    def NewRecord(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def NewReference(self, x, ref_y):
        self.ref_x.append(x)
        self.ref_y.append(ref_y)
    
    def ClearRecords(self):
        self.x, self.y = [], []

    def ClearReference(self):
        self.ref_x, self.ref_y = [], []

    def FrameFormat(self):
        data_dic = {'title':'Yield-Curve', 
            'content':[{'x':self.x, 'y':self.y, 'name':'real', 'color':'red'},
                        {'x':self.ref_x, 'y':self.ref_y, 'name':'reference', 'color':'black'}]}
        return data_dic

