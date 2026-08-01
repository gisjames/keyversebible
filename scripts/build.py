import argparse, subprocess, sys
from validate import validate
from generate_books import generate as generate_books
from generate_indexes import generate as generate_indexes

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--generate-only',action='store_true')
    p.add_argument('--format',choices=['html','pdf','epub'])
    args=p.parse_args()
    errors,warnings=validate(True)
    if errors:
        print('Build stopped: workbook validation failed.')
        return 1
    b,c=generate_books(); generate_indexes()
    print(f'Generated {b} book pages containing {c} chapters.')
    if args.generate_only: return 0
    cmd=['quarto','render']
    if args.format: cmd += ['--to',args.format]
    try: return subprocess.call(cmd)
    except FileNotFoundError:
        print('Quarto was not found on PATH. Generation completed; install Quarto to render outputs.')
        return 2

if __name__=='__main__': sys.exit(main())
