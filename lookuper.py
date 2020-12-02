#!/usr/bin/python3

# ====== LOOKUPER.PY [Ver. 0.2] ==========================================
# Descubridor de hosts mediante consultas DNS dentro de una red
# El concepto es bruteforce para DNS
# Guillo (github.com/0xGC)
# Noviembre 2020
#
# dependencias externas:
#     colorama
#     yaspin
# ========================================================================

# Cosas que le faltan:
# - poder decidir en que exportarlo (si csv o html o xml)
# - Usar threads para paralelizar el trabajo y decrementar el tiempo
# - Usar libreria DNS de python (para dejar de usar nslookup)

import subprocess as sprc
import csv
import re
from yaspin import yaspin
from colorama import Fore
from colorama import Style
import ipaddress as ipa
import argparse
version = "Version 0.2"
banner= f'''
    {Fore.RED}██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗
    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗██╔════╝██╔══██╗
    ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝█████╗  ██████╔╝{Fore.RESET}
    ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗
    ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     ███████╗██║  ██║
    {Fore.RED}╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝{Fore.RESET}
===| ### {Fore.RED}{Style.BRIGHT}DNS BRUTEFORCER {Fore.RESET}[{version}]{Style.RESET_ALL} ###  |=======[{Fore.GREEN}github.com/0xGC{Fore.RESET}]====>
'''

parser = argparse.ArgumentParser(description='DNS Bruteforcer de reconocimiento')
parser.add_argument('ip_range',
                    help="Rango de IPs en notacion CIDR (ej:192.168.1.0/24)")
parser.add_argument('--sep', default=',',
                    help="formato del separador (por defecto: , ")                    

args = parser.parse_args()
pattern = re.compile(r'\bname = .*')

sip = re.sub(r'\D','_', args.ip_range)
outfilename = sip + "_output.csv"
f = open(outfilename,'w')
writer = csv.writer(f)
print(banner)
with yaspin(text="Bucando...", color="yellow") as sp:
    for ip in ipa.IPv4Network(args.ip_range):    
        sp.text=f"Rango en {ip}"
        cmd = sprc.run(['nslookup',str(ip)],stdout=sprc.PIPE,)
        out = cmd.stdout.decode('utf-8')
        try:
            name = pattern.search(out).group()
            name = name[7:]
            sp.write(f"Host {Fore.BLUE}{name}{Fore.RESET} encontrado en {Fore.GREEN}{ip}{Fore.RESET}")
            csv_out = [ip,name]
            writer.writerow(csv_out)
        except:
            pass
    sp.text = "Escaneo de DNS completado!"
    sp.ok("*")
    sp.write(f'Archivos escritos en {Fore.GREEN}{Style.BRIGHT}{outfilename}{Style.RESET_ALL}{Fore.RESET}')