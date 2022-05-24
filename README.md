# Lookuper
Lookuper is a simple python3 script to check hosts using DNS resolve in a range (CIDR notation).
Prints the host discovery and generate a csv file.
Usefull to dump information about assets from an internal DNS
## Usage
```usage: lookuper.py [-h] [--sep SEP] [--screen] [--workers WORKERS] [--dns DNS] ip_range

DNS Bruteforcer de reconocimiento

positional arguments:
  ip_range              Rango de IPs en notacion CIDR (ej:192.168.1.0/24)

optional arguments:
  -h, --help            show this help message and exit
  --sep SEP, -s SEP     formato del separador (por defecto: ,
  --screen, -scr        Solo output por pantalla
  --workers WORKERS, -w WORKERS
                        Numero de threads concurrentes
  --dns DNS, -d DNS     Servidor DNS al que hacer las consultas

  ```

## To Do:
- Mess with error codes
