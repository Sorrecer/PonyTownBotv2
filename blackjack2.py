import random

def hit_card():
    return random.randint(1, 10)

def blackjack():
    # Mulai dengan kartu pertama untuk pemain
    player_total = hit_card()
    print(f"Kartu anda: {player_total}")
    
    # Giliran pemain
    while True:
        choice = input("Hit atau Stand? ").lower()
        
        if choice == "hit":
            new_card = hit_card()
            player_total += new_card
            print(f"Kartu baru: {new_card}, Total kartu anda: {player_total}")
            
            if player_total > 21:
                print("Anda kalah! Total kartu lebih dari 21.")
                return
        elif choice == "stand":
            print(f"Anda memilih stand dengan total kartu: {player_total}")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih 'hit' atau 'stand'.")
    
    # Giliran dealer
    dealer_total = hit_card()
    print(f"Kartu dealer: {dealer_total}")
    
    while dealer_total < 17:
        new_card = hit_card()
        dealer_total += new_card
        print(f"Kartu baru dealer: {new_card}, Total kartu dealer: {dealer_total}")
    
    if dealer_total > 21:
        print("Dealer kalah! Total kartu lebih dari 21.")
    else:
        print(f"Dealer berhenti dengan total kartu: {dealer_total}")
    
    # Menentukan pemenang
    if player_total > dealer_total or dealer_total > 21:
        print("Selamat! Anda menang!")
    elif player_total < dealer_total:
        print("Anda kalah! Dealer menang!")
    else:
        print("Seri!")

if __name__ == "__main__":
    blackjack()
