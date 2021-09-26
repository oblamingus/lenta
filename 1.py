import re
import urllib.request
import urllib.parse
import sys
import json

url_fp=''
url_s=''
a=input('Введие URL:')
b=a.split('#')
a=urllib.parse.unquote(b[1])
print(a)
c=a.split('&')
for i in (c[1:]):
    if 's=' in i:
        url_s=i
    if 'fp=' in i:
        url_fp=i

if (url_fp != '' and url_s != ''):
    tax_com_url="https://receipt.taxcom.ru/v01/show?{}&{}&sf=False&sfn=False".format(url_fp,url_s)
    for x in range(5): #Будет 5 попыток получить данные
        print("{}\tGET {}".format(x,tax_com_url))
        g = urllib.request.urlopen(tax_com_url)
        if (g.status==200 and g.length>0):
            break
    else:
        sys.exit
    content = g.read()
    a = content.decode('utf-8')
    a=a.replace('\n',' ')

    these_regex='span class="value receipt-value-(.+?)".*?>(.*?)</span>'
    pattern=re.compile(these_regex)

    x=re.findall(pattern,a)
    result_json={}
    check_items=[]
    for i in x:
        if i[0] == '1042':
            result_json.update({'num':i[1].strip()})
        if i[0] == '1012':
            result_json.update({'date':i[1].strip()})
        if i[0] == '1030':
            item_name=i[1].strip()
            item_cnt=''
            item_price=''
            item_sum=''
        if i[0] == '1023':
            item_cnt=i[1].strip()
        if i[0] == '1079':
            item_price=i[1].strip()
        if i[0] == '1043':
            item_sum=i[1].strip()
            check_items.append({'name':item_name,'price':item_price,'count':item_cnt,'sum':item_sum})
            #print('{}|{}|{}|{}|{}|{}'.format(chek_num,chek_date,item_name,item_price,item_cnt,item_sum))
        if i[0] == '1081':
            result_json.update({'total':i[1].strip()})
    result_json.update({'items':check_items})
    print(json.dumps(result_json,indent=4,ensure_ascii=False))
