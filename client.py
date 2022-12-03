from pathlib import Path
import time
import csv
import re


def client_csv_getpath(filepath):
    source_file_name = [sourcei.name for sourcei in Path(filepath).iterdir()]
    source_re_name = re.findall(r'\d+-\d+-\d+_\d+.csv', str(source_file_name))
    souece_path_curr = filepath + '\\' + source_re_name[-1]
    souece_path_last = filepath + '\\' + source_re_name[-2]
    return {'curr': souece_path_curr, 'last': souece_path_last}


def client_csv_read(filepath):
    with open(filepath, 'r') as f:
        client_csv_list = list(csv.reader(f))[2:]
        client_infotable = []
        for i in client_csv_list:
            line = (i[0], i[1], i[3], i[8])
            client_infotable.append(line)
    return client_infotable


def whitelist_write(clientinfo, factory):
    if factory == 'B01_F1':
        whitelist_path = 'txtlib/F1whitelist.txt'
    elif factory == 'B01_F2':
        whitelist_path = 'txtlib/F2whitelist.txt'
    elif factory == 'B02':
        whitelist_path = 'txtlib/B02whitelist.txt'
    else:
        return None
    nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
    with open(whitelist_path, 'a') as whitelist:
        for buffline in clientinfo:
            buffer = list(buffline)
            buffer.append(nowtime)
            whitelist.write('&' + '\t'.join(buffer) + '\n')


def whitelist_read(factory):
    if factory == 'B01_F1':
        whitelist_path = 'txtlib/F1whitelist.txt'
    elif factory == 'B01_F2':
        whitelist_path = 'txtlib/F2whitelist.txt'
    elif factory == 'B02':
        whitelist_path = 'txtlib/B02whitelist.txt'
    else:
        return None
    with open(whitelist_path, 'r') as whitelist:
        white_list = re.findall(r'&(.*?)\t(.*?)\t(.*?)\t(.*?)\t(\d+-\d+-\d+ \d+:\d+)\n', whitelist.read())
    return white_list


def double_com(basictable, targtable):
    if len(basictable[0]) >= 5:
        basic_com = [buffer[2:-1] for buffer in basictable]
    else:
        basic_com = [buffer[2:] for buffer in basictable]
    targ_com = [buffer[2:] for buffer in targtable]
    difference = []
    for buffer in targ_com:
        if buffer in basic_com:
            pass
        else:
            for diff_line in targtable:
                if diff_line[2] == buffer[0] and diff_line[3] == buffer[1]:
                    diff_index = list(targtable).index(diff_line)
                    difference.append(targtable[diff_index])
    return difference


def ill_filt(basictable):
    years = []
    ill_oa = []
    ill_assets = []
    for line in basictable:
        segment = re.findall(r'\d+\.\d+\.(\d+)\.\d+', line[0])[0]
        if segment in ('12', '117', '191'):
            pass
        elif re.findall(r'^[Q, q]\d\d\w\d\d\d\d\d\d', line[3]):
            name = line[3]
            if 'pegatron' in name:
                ill_oa.append(line)
            elif int(name[1:3]) < 12:
                years.append(line)
            else:
                pass
        else:
            ill_assets.append(line)
    return ill_assets, ill_oa, years

def html_spawn(online, offline, factory):
    if factory == 'B01_F1':
        factory_txt = 'B01-F1厰'
    elif factory == 'B01_F2':
        factory_txt = 'B01-F2厰'
    elif factory == 'B02':
        factory_txt = 'B02厰'
    else:
        factory_txt = factory
    head = '''<!DOCTYPE html><html lang="en">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>SFIS Client</title>
            <style type="text/css">
                h3.title {font-family: Microsoft YaHei; font-size:25px; color:#FFFFFF; background:#407a9f;}
                </style>
            </head>
        <body>
        <h3 align="center" class="title">SFIS網絡准入稽查</h3>'''
    online_table = '<font color="407a9f" size="3" face="微軟正黑體">{factory}無新增Client</font><br>'.format(factory=factory_txt)
    if online:
        ippool_17_20 = {17: 'BN01-02', 18: 'BN03', 19: 'BN04', 20: 'BN05'}
        ippool_39_50 = {39: '1FEPSON', 40: 'SMT', 41: 'BN01-02', 42: 'BN15-16', 43: 'BN05', 44: 'error',
                        45: 'BN13-14', 46: 'BN11-12', 47: 'Rework', 48: 'BN09-10', 49: 'BN03-04', 50: 'ETE'}
        ippool_122_126 = {122: 'BN01-04.AOI', 123: 'BN05-08.AOI', 124: 'BN09-12.AOI', 125: 'BN13-16.AOI', 126: '線外AOI'}
        ippool_128_135 = {128: 'CO01', 129: 'GN03', 130: 'BN30', 131: 'BN28-29', 132: 'BN26-27', 133: 'BN24-25', 134: 'BN22-23',
                          135: 'BN20-21'}
        ippool_172_177 = {172: 'BN17', 173: 'BN18', 174: 'BN19', 175: 'BMU01-02', 176: 'BMU03-04', 177: 'UXxianwai'}
        ippool_216_220 = {216: 'BN25-30.AOI', 217: 'BN22-24.AOI', 218: 'BN20-21.AOI', 219: 'BN17-19.AOI', 220: '.AOI'}
        online_table = '''
            <font color="407a9f" size="3" face="微軟正黑體">以下為{factory}新增Client</font>
            <table border="1" style="border-collapse: collapse;" width="900">
            <tbody>
            <tr>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">IP</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">主機名</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">MAC</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">網段</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">線別</font></th>
            </tr>'''.format(factory=factory_txt)
        for buffer in online:
            pool = re.findall(r'\d+\.(\d+)\.(\d+)\.\d+', buffer[1])[0]
            ask = int(pool[1])
            if pool[0] == '9':
                location = 'B02'
            elif ask in (12, 117, 191):
                location = 'NetworkAP'
            elif ask in range(17, 21):
                location = ippool_17_20[ask]
            elif ask in range(39, 51):
                location = ippool_39_50[ask]
            elif ask in range(122, 127):
                location = ippool_122_126[ask]
            elif ask in range(128, 136):
                location = ippool_128_135[ask]
            elif ask in range(172, 178):
                location = ippool_172_177[ask]
            elif ask in range(216, 221):
                location = ippool_216_220[ask]
            else:
                location = 'Unknown'
            online_table += '''<tr>
                <td align="center"><font size="2" face="微軟正黑體">{ip}</font></td>
                <td><font size="2" face="微軟正黑體">{name}</font></td>
                <td align="center"><font size="2" face="微軟正黑體">{mac}</font></td>
                <td align="center"><font size="2" face="微軟正黑體">{wd}</font></td>
                <td align="center"><font size="2" face="微軟正黑體">{lineb}</font></td>
                </tr>'''.format(lineb=location, ip=buffer[0], wd=buffer[1], mac=buffer[2], name=buffer[3])
        online_table += '''</tbody>
        </table>'''
    offline_table = '</font><font color="407a9f" size="3" face="微軟正黑體">{factory}無新離綫Client</font><br>'.format(factory=factory_txt)
    if offline:
        ippool_17_20 = {17: 'BN01-02', 18: 'BN03', 19: 'BN04', 20: 'BN05'}
        ippool_39_50 = {39: '1FEPSON', 40: 'SMT', 41: 'BN01-02', 42: 'BN15-16', 43: 'BN05', 44: 'error',
                        45: 'BN13-14', 46: 'BN11-12', 47: 'Rework', 48: 'BN09-10', 49: 'BN03-04', 50: 'ETE'}
        ippool_122_126 = {122: 'BN01-04.AOI', 123: 'BN05-08.AOI', 124: 'BN09-12.AOI', 125: 'BN13-16.AOI', 126: '線外AOI'}
        ippool_128_135 = {128: 'CO01', 129: 'GN03', 130: 'BN30', 131: 'BN28-29', 132: 'BN26-27', 133: 'BN24-25', 134: 'BN22-23',
                          135: 'BN20-21'}
        ippool_172_177 = {172: 'BN17', 173: 'BN18', 174: 'BN19', 175: 'BMU01-02', 176: 'BMU03-04', 177: 'UXxianwai'}
        ippool_216_220 = {216: 'BN25-30.AOI', 217: 'BN22-24.AOI', 218: 'BN20-21.AOI', 219: 'BN17-19.AOI', 220: '.AOI'}
        offline_table = '''
                    <font color="407a9f" size="3" face="微軟正黑體">以下為{factory}離綫Client</font>
                    <table border="1" style="border-collapse: collapse;" width="900">
                    <tbody>
                    <tr>
                    <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">IP</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">主機名</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">MAC</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">網段</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">線別</font></th>
                    </tr>'''.format(factory=factory_txt)
        for buffer in offline:
            pool = re.findall(r'\d+\.(\d+)\.(\d+)\.\d+', buffer[1])[0]
            ask = int(pool[1])
            if pool[0] == '9':
                location = 'B02'
            elif ask in range(17, 21):
                location = ippool_17_20[ask]
            elif ask in range(39, 51):
                location = ippool_39_50[ask]
            elif ask in range(122, 127):
                location = ippool_122_126[ask]
            elif ask in range(128, 136):
                location = ippool_128_135[ask]
            elif ask in range(172, 178):
                location = ippool_172_177[ask]
            elif ask in range(216, 221):
                location = ippool_216_220[ask]
            else:
                location = 'Unknown'
            offline_table += '''<tr>
                <td align="center"><font size="2" face="微軟正黑體">{ip}</font></td>
                <td><font size="2" face="微軟正黑體">{name}</font></td>
                <td align="center"><font size="2" face="微軟正黑體">{mac}</font></td>
                <td align="center"><font size="2" face="微軟正黑體">{wd}</font></td>
                <td align="center"><font size="2" face="微軟正黑體">{lineb}</font></td>
                </tr>'''.format(ip=buffer[0], wd=buffer[1], mac=buffer[2], name=buffer[3], lineb=location)
        offline_table += '''</tbody>
                </table>'''
    end = '''</body>
        </html>'''
    html_egg = head + online_table + offline_table + end
    return html_egg


def email_send(email_to, email_cc, html_egg, factory):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    if factory == 'B01_F1':
        factory_txt = 'B01-F1'
    elif factory == 'B01_F2':
        factory_txt = 'B01-F2'
    else:
        factory_txt = 'Unknown'
    nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
    sender = 'email'
    receivers = email_to + email_cc
    
    message = MIMEText(html_egg, 'html', 'utf-8')
    subject = f'【SFIS網絡准入稽查】{factory_txt}厰SFIS Client數量異動情況 '+nowtime
    message['Subject'] = Header(subject, 'utf-8')
    msg_to = ''
    msg_cc = ''
    for i in email_to:
        msg_to += i + ';'
    for i in email_cc:
        msg_cc += i + ';'
    message['To'] = Header(msg_to)
    message['Cc'] = Header(msg_cc)

    try:
        smtpobj = smtplib.SMTP('email')
        smtpobj.sendmail(sender, receivers, message.as_string())
        print("sucess")
    except smtplib.SMTPException:
        print("Error")
