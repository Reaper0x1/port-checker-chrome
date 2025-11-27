import requests
from colorama import init, Fore, Back, Style

# Inizializza colorama
init(autoreset=True)

# URL dell'API di ciphersuite.info
base_url = "https://ciphersuite.info/api/cs/"

# Funzione per controllare lo stato di sicurezza di un cifrario tramite l'API
def check_cipher_safety(cipher):
    try:
        # Effettua una richiesta GET all'API per ottenere il cifrario
        response = requests.get(f"{base_url}{cipher}")
        
        # Se la richiesta ha successo
        if response.status_code == 200:
            data = response.json()
            
            # Ogni risposta dell'API ha come chiave il nome del cifrario
            # Prendiamo il primo (e unico) elemento della risposta
            cipher_data = data.get(cipher)
            
            if cipher_data:
                # Ora possiamo accedere al campo 'security' nel dizionario del cifrario
                security_level = cipher_data.get('security', None)
                
                if security_level:
                    # Restituiamo il livello di sicurezza (es. "secure", "insecure", "weak", "recommended")
                    return security_level
                else:
                    # Se non c'è il campo 'security', segniamo come errore
                    return "in errore"
            else:
                # Se non c'è il cifrario nella risposta
                return "in errore"
        else:
            print(f"Errore: la risposta dell'API per {cipher} ha status {response.status_code}.")
            print(f"Messaggio di errore: {response.text}")
            return "in errore"
    except requests.RequestException as e:
        print(f"Errore durante la richiesta per il cifrario {cipher}: {e}")
        return "in errore"

# Funzione per leggere i cifrari da un file e controllarne la sicurezza
def process_ciphers_from_file(file_path):
    safe_ciphers = []
    unsafe_ciphers = []
    error_ciphers = []
    all_ciphers = set()  # Usato per tenere traccia dei cifrari già visti (senza duplicati)
    duplicate_ciphers = set()  # Usato per tenere traccia dei duplicati trovati

    # Legge il file contenente i cifrari
    try:
        with open(file_path, 'r') as file:
            # Itera su ciascuna riga (cifrario)
            for line in file:
                cipher = line.strip()  # Rimuove eventuali spazi o newline
                if cipher:  # Verifica che la riga non sia vuota
                    if cipher in all_ciphers:
                        # Se il cifrario è già stato visto, aggiungilo ai duplicati
                        duplicate_ciphers.add(cipher)
                    else:
                        # Aggiungi il cifrario all'insieme di cifrari già visti
                        all_ciphers.add(cipher)
                        print(f"{Fore.YELLOW}Verificando il cifrario: {Fore.CYAN}{cipher}")
                        security_level = check_cipher_safety(cipher)
                        if security_level == "secure":
                            safe_ciphers.append(cipher)
                        elif security_level in ["insecure", "weak", "recommended"]:
                            unsafe_ciphers.append(cipher)
                        else:
                            error_ciphers.append(cipher)
    except FileNotFoundError:
        print(f"{Fore.RED}Errore: il file {file_path} non è stato trovato.")
    except Exception as e:
        print(f"{Fore.RED}Errore nel processare il file: {e}")

    return safe_ciphers, unsafe_ciphers, error_ciphers, duplicate_ciphers

# File che contiene la lista di cifrari
file_path = "ciphers.txt"  # Cambia con il percorso del tuo file

# Processa i cifrari dal file
safe_ciphers, unsafe_ciphers, error_ciphers, duplicate_ciphers = process_ciphers_from_file(file_path)

# Risultato finale
print(f"\n{Fore.GREEN}Numero di cifrari sicuri: {len(safe_ciphers)}")
print(f"{Fore.RED}Numero di cifrari non sicuri: {len(unsafe_ciphers)}")
print(f"{Fore.YELLOW}Numero di cifrari con errore: {len(error_ciphers)}")

# Mostra le liste dei cifrari sicuri, non sicuri e con errore
print(f"\n{Fore.GREEN}{Style.BRIGHT}Cifrari sicuri:")
for cipher in safe_ciphers:
    print(f"- {Fore.GREEN}{cipher}")

print(f"\n{Fore.RED}{Style.BRIGHT}Cifrari non sicuri:")
for cipher in unsafe_ciphers:
    print(f"- {Fore.RED}{cipher}")

print(f"\n{Fore.YELLOW}{Style.BRIGHT}Cifrari con errore:")
for cipher in error_ciphers:
    print(f"- {Fore.YELLOW}{cipher}")

# Mostra i duplicati, se ce ne sono
if duplicate_ciphers:
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}Cifrari duplicati trovati e ignorati:")
    for cipher in duplicate_ciphers:
        print(f"- {Fore.MAGENTA}{cipher}")
