import poplib
import re
from decimal import Decimal
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


import html5lib
from bs4 import BeautifulSoup


# indent用于缩进显示:
def print_info(msg, indent=0, if_print=True):
    cc = ''
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            if if_print:
                print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            if if_print:
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))

            content = print_info(part, indent + 1)
            if len(content) > 10:
                cc = content
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            if if_print:
                print('%sText: %s' % ('  ' * indent, content + '...'))
            if len(content) > 10:
                cc = content
        else:
            if if_print:
                print('%sAttachment: %s' % ('  ' * indent, content_type))
    return cc


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_data(number_of_mail=5, email='huangjy@founderff.com', password='Abc12345', pop3_server='mail.founderff.com'):
    # 输入邮件地址, 口令和POP3服务器地址:

    # 连接到POP3服务器:
    server = poplib.POP3(pop3_server)
    # 可以打开或关闭调试信息:
    server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))

    # 身份认证:
    server.user(email)
    server.pass_(password)

    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails) - number_of_mail
    resp, lines, octets = server.retr(index)

    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)

    content = print_info(msg)

    # searchObj = re.search( r'(.*) <html (.*?)</html> (.*?).*', msg, re.M|re.I)
    # if searchObj:
    #    print("searchObj.group() : ", searchObj.group())
    #    print("searchObj.group() : ", searchObj.group(1))
    #    print("searchObj.group() : ", searchObj.group(2))
    # else:
    #    print("Nothing found!!")

    def normalize(name, value):
        s = ''
        for each in name[:-1]:
            s += each.contents[0].encode().decode().strip()
        if value == '-' or value == '':
            value = '0'
        s=s.replace('：','')
        return s, value.replace(',', '')

    soup = BeautifulSoup(content)
    htmltext = soup.prettify()
    stored = {}
    stored_list = []
    title = ''
    for each in soup.find_all('tr')[0].find_all('p')[0].find_all('span')[0].contents[:-1]:
        title += each.encode().decode().strip()
    if title == '深<span lang="EN-US">100ETF</span>联接头寸表':
        title = '深100ETF联接头寸表'

    for i in soup.find_all('tr')[1:]:
        i.find_all('p')
        if len(i.find_all('p')) < 2:
            continue

        k, v = normalize(i.find_all('p')[0].find_all('span'),
                         i.find_all('p')[1].find('span').contents[0].encode().decode().strip())
        stored[k] = v
        stored_list.append((k, v))
    # 关闭连接:
    server.quit()
    print(title,stored)
    return title, stored


if __name__ == '__main__':
    get_data(9)
