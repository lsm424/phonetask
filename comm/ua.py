#encoding=utf-8
import csv
import os
import random


class PhoneUA:
    def __init__(self):
        path = os.path.join(os.path.split(__file__)[0], 'ua_string .csv')
        csv_file = csv.reader(open(path, 'r', encoding='gb2312'))
        self.PhoneUA = filter(lambda x: len(x) > 0 and ('iPhone' in x[0] or 'Android' in x[0]), csv_file)
        self.PhoneUA = list(map(lambda x: x[0], self.PhoneUA))

    def get_ua(self):
        return random.choice(self.PhoneUA)


ua = PhoneUA()

if __name__ == '__main__':
    print(ua.get_ua())
    print(ua.get_ua())
    print(ua.get_ua())
    print(ua.get_ua())
    print(ua.get_ua())
