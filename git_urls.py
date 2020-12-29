import os
import argparse
import sys
import requests
import json
import pyfiglet
import pandas as pd
from progress.bar import Bar

version = 'BETA'


def banner():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    ascii_banner = pyfiglet.figlet_format("GIT URLS")
    print(ascii_banner)
    print('[>]' + ' Created by : ' + 'sh4d0wn13')
    print('[>]' + ' Version    : ' + version + '\n')
    
def check_api(token):
    try:
        parameters = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
                      'Accept': 'application/vnd.github.v3+json'}
        rqst = requests.get('https://api.github.com/search/code?access_token={}'.format(
        token), headers=parameters, timeout=16)
        json_out = rqst.content.decode('utf-8', 'ignore')
        sc = rqst.status_code
        if sc == 200:
            data = sc
        else:
            data = sc
        return data
    except:
        print('Ocurrio un error :s')


def api_key():
    global key
    try:
        with open('key.txt', 'r') as keyfile:
            key = keyfile.readline()
            key = key.strip()
            print('[+]' + ' API Key Funciona...' + '\n')
    except FileNotFoundError:
        print('[+]' + ' Consigua su API Key : ' +
              'https://github.com/settings/tokens')
        key_validation = False
        while key_validation != True:
            enter_key = input('[+]' + ' Ingrese su API Key : ')
            if check_api(enter_key) == 401:
                print('[-]' + ' API Key Not Funciona, por favor intentelo de nuevo' + '\n')
            else:
                key_validation = True
        key = enter_key.strip()
        with open('key.txt', 'w') as keyfile:
            keyfile.write(enter_key)
        key_path = os.getcwd() + '/key.txt'
        print('[+]' + ' API Key Guardada en : ' + key_path + '\n')

def company_name():
    global company
    company = input('[+]' + ' Ingrese el nombre del objetivo: ')
    company = company.strip()

def out_file_name():
    global out_file
    out_file = input(
        '[+]' + ' Ingrese el nombre para el archivo de salida : ')

def request_github(company, page, token):
    try:
        parameters = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
                      'Accept': 'application/vnd.github.v3+json'}
        rqst = requests.get('https://api.github.com/search/code?q="{}"&per_page=100&page={}&access_token={}'.format(
            company, page, token), headers=parameters, timeout=16)
        json_out = rqst.content.decode('utf-8', 'ignore')
        sc = rqst.status_code
        if sc == 200:
            data = json_out
        else:
            data = False
        return data
    except:
        print('Ocurrio un error :s')


def page_numbers(results_numbers):
    if results_numbers > 100 and results_numbers <= 1000:
        pages = results_numbers//100
        print(results_numbers)
        if (results_numbers % 100) > 0:
            pages += 1
    elif results_numbers > 100 and results_numbers > 1000:
        pages = 10
    else:
        pages = 1
    return pages


banner()
api_key()
company_name()
out_file_name()
results = json.loads(request_github(company, 1, key))
results_number = results['total_count']
pages_number = page_numbers(int(results_number))
names = []
urls = []

print('Numero de paginas: ' + str(pages_number) + '\n')
with Bar('Procesando', max=pages_number) as bar:
    while pages_number > 0:
        data = json.loads(request_github(company, pages_number, key))
        for item in data['items']:
            names.append(item['name'])
            urls.append(item['html_url'])
        pages_number -= 1
        bar.next()


datos = {"nombres": names, "urls": urls}
datos_json = json.dumps(datos)
df = pd.DataFrame(datos, columns=['nombres', 'urls'])
print('\nPrevisualización: ' + '\n')
print(df)
filename = out_file + '.xlsx'
try:
    df.to_excel(filename, index=False, header=True)
    results_path = os.getcwd() + '/' + filename
    print('\n[+]' + ' Resultados guardados en: ' + results_path)
except:
    print('[-]' + ' Error en crear el archivo: ' + filename)