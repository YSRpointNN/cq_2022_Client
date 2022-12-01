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
    else:
        return None
    with open(whitelist_path, 'r') as whitelist:
        white_list = re.findall(r'&(.*?)\t(.*?)\t(.*?)\t(.*?)\t(\d+-\d+-\d+ \d+:\d+)\n', whitelist.read())
    return white_list


def double_com(basictable, targtable):
    difference = []
    if len(basictable[0]) >= 5:
        basic_com = [buffer[2:-1] for buffer in basictable]
    else:
        basic_com = [buffer[2:] for buffer in basictable]
    targ_com = [buffer[2:] for buffer in targtable]
    for buffer in targ_com:
        if buffer in basic_com:
            pass
        else:
            for diff_line in targtable:
                if diff_line[2] == buffer[0] and diff_line[3] == buffer[1]:
                    diff_index = list(targtable).index(diff_line)
                    difference.append(targtable[diff_index])
    return difference


def html_spawn(online, offline, factory):
    if factory == 'B01_F1':
        factory_txt = 'B01-F1'
    elif factory == 'B01_F2':
        factory_txt = 'B01-F2'
    else:
        factory_txt = 'Unknown'
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
    online_table = '<font color="407a9f" size="3" face="微軟正黑體">{factory}厰無新增Client</font><br>'.format(factory=factory_txt)
    if online:
        online_table = '''
            <font color="407a9f" size="3" face="微軟正黑體">以下為{factory}新增Client</font>
            <table border="1" style="border-collapse: collapse;" width="900">
            <tbody>
            <tr>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">IP</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">網段</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">MAC</font></th>
                <th bgcolor="407a9f"><font color="ffffff" size="2" face="微軟正黑體">主機名</font></th>
            </tr>'''.format(factory=factory_txt)
        for buffer in online:
            online_table += '''<tr>
                <td align="center"><font size="1" face="微軟正黑體">{ip}</font></td>
                <td align="center"><font size="1" face="微軟正黑體">{wd}</font></td>
                <td align="center"><font size="1" face="微軟正黑體">{mac}</font></td>
                <td align="center"><font size="1" face="微軟正黑體">{name}</font></td>
                </tr>'''.format(ip=buffer[0], wd=buffer[1], mac=buffer[2], name=buffer[3])
        online_table += '''</tbody>
        </table>'''
    offline_table = '</font><font color="407a9f" size="3" face="微軟正黑體">{factory}厰無新離綫Client</font><br>'.format(factory=factory_txt)
    if offline:
        offline_table = '''
                    <font color="407a9f" size="3" face="微軟正黑體">以下為{factory}離綫Client</font>
                    <table border="1" cellpadding="0" cellspacing="0" width="900">
                    <tbody>
                    <tr>
                    <th bgcolor="407a9f"><font color="ffffff" size="1" face="微軟正黑體">IP</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="1" face="微軟正黑體">網段</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="1" face="微軟正黑體">MAC</font></th>
                    <th bgcolor="407a9f"><font color="ffffff" size="1" face="微軟正黑體">主機名</font></th>
                    </tr>'''.format(factory=factory_txt)
        for buffer in offline:
            offline_table += '''<tr>
                        <td align="center"><font color="407a9f" size="1" face="微軟正黑體">{ip}</font></td>
                        <td align="center"><font color="407a9f" size="1" face="微軟正黑體">{wd}</font></td>
                        <td align="center"><font color="407a9f" size="1" face="微軟正黑體">{mac}</font></td>
                        <td align="center"><font color="407a9f" size="1" face="微軟正黑體">{name}</font></td>
                        </tr>'''.format(ip=buffer[0], wd=buffer[1], mac=buffer[2], name=buffer[3])
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
    sender = 'PCQ_MIS_RPA@intra.pegatroncorp.com'
    to = [email_to]
    cc = [email_cc]
    receivers = to + cc

    message = MIMEText(html_egg, 'html', 'utf-8')
    subject = f'【SFIS網絡准入稽查】{factory_txt}厰SFIS Client數量異動情況'
    message['Subject'] = Header(subject, 'utf-8')
    message['To'] = Header(email_to)
    message['Cc'] = Header(email_to)

    try:
        smtpobj = smtplib.SMTP('relay.cq.pegatroncorp.com')
        smtpobj.sendmail(sender, receivers, message.as_string())
        print("sucess")
    except smtplib.SMTPException:
        print("Error")
