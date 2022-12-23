from LIS_Client import LIS

lis = LIS()

DATA = open('XN550.txt', 'r')
RAW_INCOMING_FRAME = DATA.readline();

if lis.load_lis_data(RAW_INCOMING_FRAME):
    print(lis.get_lis_result())
else:
    print(lis.get_lis_error())