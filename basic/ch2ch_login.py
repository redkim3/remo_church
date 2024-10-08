import pandas as pd

def ch2ch_Id():
    ch2ch_id = pd.read_excel('./DB/ch2ch.xlsx',sheet_name="ch2ch", header=0, index_col=None) #, names=None)
    return ch2ch_id

def ch2chID_select():
    ch2chid = ch2ch_Id()
    IDPW = ch2chid['ID'][['ID','pw']]
    return IDPW