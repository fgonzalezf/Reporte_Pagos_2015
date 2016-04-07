__author__ = 'fgonzalezf'
import datetime
rec=0
def fecha(campo):
    global rec
    if (rec == 0):
        rec =datetime.datetime.now()
    else:
        rec = rec + datetime.timedelta(days=1)
    return rec
