#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# ====== LOOKUPER.PY [Ver. 0.2] ==========================================
# Descubridor de hosts mediante consultas DNS dentro de una red
# El concepto es "bruteforce" para DNS
# Guillo (github.com/0xGC)
# Noviembre 2020
#
# dependencias externas:
#     colorama
#     yaspin
#     dns
# ========================================================================

# Cosas que le faltan:
# - poder decidir en que exportarlo (si csv o html o xml)

from dns import resolver, reversename, exception
import csv
from yaspin import yaspin
import ipaddress as ipa
import argparse
import re
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style
from concurrent.futures import ThreadPoolExecutor, as_completed



def pinta (rollo, text1, text2=''):
    if rollo == "good":
        ico = "[+]"
        style = Style.from_dict({
        'icon': '#4caf50',
        'msg': 'bold',
        'sub-msg': '#cccccc italic'
        })

    elif rollo == "bad":
        ico = "[-]"
        style = Style.from_dict({
        'icon': '#e0300a bold',
        'msg': 'bold',
        'sub-msg': '#cccccc italic'
        })
    
    elif rollo == "warn":
        ico = "[-]"
        style = Style.from_dict({
        'icon': '#ffc900',
        'msg': 'bold',
        'sub-msg': '#cccccc italic'
        })

    with sp.hidden():
        print_formatted_text(HTML(
            f'<b><icon>{ico}</icon></b> <msg>{text1}</msg> <sub-msg>{text2}</sub-msg>'
        ), style=style)

version = "0.5"

def banner(): 
    style = Style.from_dict({
    'ban': '#167cc7',
    'sub-ban': '#a6ffeb italic',
    'text': '#4fabd6',
    'version': '#8103f8 bold'
    })
    print_formatted_text(HTML(f'''<ban>
    ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗
    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗██╔════╝██╔══██╗
    ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝█████╗  ██████╔╝</ban><sub-ban>
    ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗
    ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     ███████╗██║  ██║
    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝</sub-ban><text>
    ===| ### DNS BRUTEFORCER [</text><version>{version}</version><text>] ###  |=======[</text><version>github.com/0xGC</version><text>]====></text>
    '''), style=style)

parser = argparse.ArgumentParser(description='DNS Bruteforcer de reconocimiento')
parser.add_argument('ip_range',
                    help="Rango de IPs en notacion CIDR (ej:192.168.1.0/24)")
parser.add_argument('--sep','-s', default=',',
                    help="formato del separador (por defecto: , ")
parser.add_argument('--screen','-scr', help="Solo output por pantalla", action='store_true')
parser.add_argument('--workers','-w', type=int, help="Numero de threads concurrentes", default=10)
parser.add_argument('--dns','-d', help="Servidor DNS al que hacer las consultas", default=False)                         


args = parser.parse_args()
pattern = re.compile(r'\bname = .*')

def consulta_dns(ip):
    try:
        addr=reversename.from_address(str(ip))
        name = str(resolver.resolve(addr,"PTR")[0])
        pinta("good",f"{name}({addr})",f"encontrado en {ip}")
        if not args.screen:
            csv_out = [ip,name]
            writer.writerow(csv_out)
    except resolver.NXDOMAIN:
        pass
        # No tengo mucha idea porque la variable no se va al main :( queria hacer un contador de timeouts, pero no
        # consigo sacarlo ...
        # sp.write("Algo!")
        # counter = counter + 1
        # sp.write(f"Timeouts Recibidos: {counter}")
    
    except resolver.NoNameservers:
        pinta("bad",f"La ip {ip} devuelve cosas chungas")



sip = re.sub(r'\D','_', args.ip_range)

if not args.screen: 
    outfilename = sip + "_output.csv"
    f = open(outfilename,'w')
    writer = csv.writer(f)


if __name__ == "__main__":
    banner()
    processes = []
    if args.dns:
        resolver.default_resolver = resolver.Resolver(configure=False)
        resolver.default_resolver.nameservers = [args.dns]
    with yaspin(text=f"Bucando en {args.ip_range}").blue.bold.shark.blue as sp:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            for ip in ipa.IPv4Network(args.ip_range):
                sp.text=f"Bucando en {args.ip_range}"   
                processes.append(executor.submit(consulta_dns, ip))

        for task in as_completed(processes):
            if task.result() is None:
                pass
            else:
                print(task.result())

        sp.text = "Escaneo de DNS completado!"
        sp.green.ok("✔")

        if not args.screen:
            pinta("good", f'Archivos escritos en {outfilename}' )
