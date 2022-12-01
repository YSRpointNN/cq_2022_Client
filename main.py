from PEGA_client import *
EMAIL_TO = 'is a email'
EMAIL_CC = 'is a email'
SOURCE_PATH = r'\\10.8.60.23\d\DHCP_Lease'
FACTORY = 'B01_F1'

# start-------------------------------------------------------#
PathLoad = client_csv_getpath(SOURCE_PATH)
CurrClientTable = client_csv_read(PathLoad['curr'])
LastClientTable = client_csv_read(PathLoad['last'])
WhiteListTable = whitelist_read(FACTORY)
OnLine = double_com(WhiteListTable, CurrClientTable)
OffLine = double_com(CurrClientTable, LastClientTable)
whitelist_write(OnLine, FACTORY)
html = html_spawn(OnLine, OffLine, FACTORY)
email_send(EMAIL_TO, EMAIL_CC, html, FACTORY)
