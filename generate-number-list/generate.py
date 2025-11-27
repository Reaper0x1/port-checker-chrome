def get_integer_input(prompt):
    """Funzione per validare l'input dell'utente come numero intero"""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Errore: inserisci un numero intero valido!")

def generate_number_file():
    """Genera un file con una sequenza di numeri"""
    print("=== Generatore di sequenza numerica ===\n")
    
    # Richiesta input dall'utente
    start = get_integer_input("Inserisci il numero iniziale: ")
    end = get_integer_input("Inserisci il numero finale: ")
    
    # Verifica che il range sia valido
    if start > end:
        print(f"\nAttenzione: il numero iniziale ({start}) è maggiore del finale ({end}).")
        print("I numeri saranno generati in ordine decrescente.")
    
    # Nome del file
    filename = f"numeri_{start}_a_{end}.txt"
    
    # Scrittura nel file
    try:
        with open(filename, 'w') as file:
            if start <= end:
                # Sequenza crescente
                for number in range(start, end + 1):
                    file.write(f"{number}\n")
            else:
                # Sequenza decrescente
                for number in range(start, end - 1, -1):
                    file.write(f"{number}\n")
        
        # Conferma operazione completata
        total_numbers = abs(end - start) + 1
        print(f"\n✓ File '{filename}' creato con successo!")
        print(f"✓ Generati {total_numbers} numeri da {start} a {end}")
        
    except Exception as e:
        print(f"\n✗ Errore durante la creazione del file: {e}")

# Esecuzione dello script
if __name__ == "__main__":
    generate_number_file()
