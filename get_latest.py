import requests, json, time, sys, os, traceback
from datetime import date

url = {
    'qxc_raw_txt' : 'http://data.17500.cn/7xc_asc.txt',
    'plw_raw_txt' : 'http://data.17500.cn/pl5_asc.txt',
    'pls_raw_txt' : 'http://data.17500.cn/pl3_asc.txt',
    'sd_raw_txt' : 'http://data.17500.cn/3d_asc.txt'
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
    'Origin': 'https://static.sporttery.cn',
    'Referer': 'https://static.sporttery.cn/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15'
}


def process(name):
    today = date.today().strftime('%Y-%m-%d')
    qxc_date = None
    qxc_value = None
    for i in range(1):
        try:
            response = requests.get(url[name], headers=headers)
            if not os.path.exists(name):
                with open(name, 'a') as f:
                    for line in response.text.split('\n'):
                        lines = line.split(' ')
                        if name == 'plw_raw_txt':
                            f.write(lines[1] + ' ' + lines[2] + " " + lines[3] + " " + lines[4] + " " + lines[5] + " " + lines[6] + '\n')
                        elif name == 'qxc_raw_txt':
                            f.write(lines[1] + ' ' + lines[2] + " " + lines[3] + " " + lines[4] + " " + lines[5] + " " + lines[6] + ' ' + lines[7] + ' ' + lines[8] + '\n')
                        elif name in ['pls_raw_txt', 'sd_raw_txt']:
                            f.write(lines[1] + ' ' + lines[2] + " " + lines[3] + " " + lines[4] + '\n')
            else:   
                raw = response.text.split('\n')[-1].split(' ')
                if raw[1] == today:
                    qxc_date = raw[1]
                    if name == 'qxc_raw_txt':
                        qxc_value = raw[2] + " " + raw[3] + " " + raw[4] + " " + raw[5] + " " + raw[6] + " " + raw[7] + " " + raw[8]
                    elif name == 'plw_raw_txt':
                        qxc_value = raw[2] + " " + raw[3] + " " + raw[4] + " " + raw[5] + " " + raw[6]
                    elif name in ['pls_raw_txt', 'sd_raw_txt']:
                        qxc_value = raw[2] + " " + raw[3] + " " + raw[4]
                    break
                else:
                    if name == 'qxc_raw_txt':
                        print(raw[1], raw[2] + " " + raw[3] + " " + raw[4] + " " + raw[5] + " " + raw[6] + " " + raw[7] + " " + raw[8])
                    elif name == 'plw_raw_txt':
                        print(raw[1], raw[2] + " " + raw[3] + " " + raw[4] + " " + raw[5] + " " + raw[6])
                    elif name in ['pls_raw_txt', 'sd_raw_txt']:
                        print(raw[1], raw[2] + " " + raw[3] + " " + raw[4])
        except Exception as e:
            print(raw)
            traceback.print_exc()
        time.sleep(10)
    if qxc_date is not None and qxc_value is not None:
        with open(name, 'a') as w:
            w.write(qxc_date + ' ' + qxc_value + '\n')
        cnt = 0
        with open(name, 'r') as r:
            for line in r:
                if '\n' in line and len(line) > 5:
                    cnt += 1
        if cnt % 2 == 1:
            print('FIXED')
        else:
            print('FIND')
    else:
        print('EMPTY')



if __name__ == '__main__':
    args = sys.argv
    process(args[1].split('_')[0] + '_raw_txt')
