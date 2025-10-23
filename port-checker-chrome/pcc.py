import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Usage: python script.py <ip/domain> <ports_file> <http|https>

def main():
    if len(sys.argv) != 4:
        print('Usage: python script.py <ip/domain> <ports_file> <http|https>')
        sys.exit(1)

    target = sys.argv[1]
    ports_file = sys.argv[2]
    protocol = sys.argv[3].lower()

    if protocol not in ['http', 'https']:
        print('Error: protocol must be http or https')
        sys.exit(1)

    try:
        with open(ports_file, 'r') as f:
            ports = [line.strip().split()[0] for line in f if line.strip()]
    except FileNotFoundError:
        print(f'Error: File {ports_file} not found.')
        sys.exit(1)

    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    total = len(ports)
    for idx, port in enumerate(ports, start=1):
        url = f'{protocol}://{target}:{port}'
        print(f'[{idx}/{total}] Loading {url}...')
        driver.get(url)
        input('Press ENTER to continue to the next port...')

    input('Last port visited. Press ENTER to close the browser and exit.')
    driver.quit()

if __name__ == '__main__':
    main()
