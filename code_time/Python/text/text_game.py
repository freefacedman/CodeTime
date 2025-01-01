import sys
import random

def start_game():
    print("==========================================")
    print(" Welcome to the Enhanced Mushroom Farming Adventure!")
    print("==========================================\n")
    print("You are about to embark on a journey to build your own mushroom farming business.")
    print("Make wise decisions each month to grow your business. Beware of risks that can lead to bankruptcy.\n")

    # Initialize player's assets
    assets = {
        'Money': 10000,            # Starting capital in dollars
        'Land': 1,                 # Acres of land
        'Equipment': 1,            # Number of equipment units
        'Mushrooms': 0,            # Current stock
        'Staff': 0,                # Number of staff hired
        'Research': 0,             # Investment in R&D
        'Debt': 0,                 # Outstanding debt
        'Month': 1,                # Current month
        'Marketing': False         # Marketing investment flag
    }

    print_current_assets(assets)
    game_loop(assets)

def print_current_assets(assets):
    print("\n--- Current Assets ---")
    for key, value in assets.items():
        print(f"{key}: {value}")
    print("----------------------\n")

def game_loop(assets):
    while True:
        print(f"=== Month {assets['Month']} ===")
        print_current_assets(assets)
        first_decision(assets)
        second_decision(assets)
        third_decision(assets)
        fourth_decision(assets)
        random_event(assets)
        financial_update(assets)
        check_game_status(assets)
        assets['Month'] += 1

def first_decision(assets):
    print("Decision 1: Expand Your Resources")
    print("1. Buy more land ($5,000 per acre)")
    print("2. Purchase additional equipment ($3,000 per unit)")
    print("3. Hire staff ($2,500 per staff member)")
    print("4. Do nothing this month")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        acres = input("How many acres would you like to buy? ")
        if acres.isdigit() and int(acres) > 0:
            cost = 5000 * int(acres)
            if assets['Money'] >= cost:
                assets['Land'] += int(acres)
                assets['Money'] -= cost
                print(f"Purchased {acres} acre(s) of land.")
            else:
                print("Not enough money to buy that much land.")
                bankruptcy()
        else:
            print("Invalid input. Must enter a positive number.")
            bankruptcy()
    elif choice == '2':
        units = input("How many equipment units would you like to buy? ")
        if units.isdigit() and int(units) > 0:
            cost = 3000 * int(units)
            if assets['Money'] >= cost:
                assets['Equipment'] += int(units)
                assets['Money'] -= cost
                print(f"Purchased {units} equipment unit(s).")
            else:
                print("Not enough money to buy that much equipment.")
                bankruptcy()
        else:
            print("Invalid input. Must enter a positive number.")
            bankruptcy()
    elif choice == '3':
        staff = input("How many staff members would you like to hire? ")
        if staff.isdigit() and int(staff) > 0:
            cost = 2500 * int(staff)
            if assets['Money'] >= cost:
                assets['Staff'] += int(staff)
                assets['Money'] -= cost
                print(f"Hired {staff} staff member(s).")
            else:
                print("Not enough money to hire that many staff members.")
                bankruptcy()
        else:
            print("Invalid input. Must enter a positive number.")
            bankruptcy()
    elif choice == '4':
        print("Chose to make no expansions this month.")
    else:
        print("Invalid choice.")
        bankruptcy()

def second_decision(assets):
    print("Decision 2: Invest in Your Business")
    print("1. Purchase high-quality mushroom spores ($2,000)")
    print("2. Invest in marketing to boost sales ($1,500)")
    print("3. Allocate funds to research & development ($2,500)")
    print("4. Do not invest this month")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        if assets['Money'] >= 2000:
            assets['Mushrooms'] += 100  # Increase potential yield
            assets['Money'] -= 2000
            print("Purchased high-quality mushroom spores. Potential yield increased by 100 mushrooms.")
        else:
            print("Not enough money to purchase spores.")
            bankruptcy()
    elif choice == '2':
        if assets['Money'] >= 1500:
            assets['Marketing'] = True
            assets['Money'] -= 1500
            print("Invested in marketing. Sales will increase this month.")
        else:
            print("Not enough money to invest in marketing.")
            bankruptcy()
    elif choice == '3':
        if assets['Money'] >= 2500:
            assets['Research'] += 1
            assets['Money'] -= 2500
            print("Invested in research & development. Future yields may improve.")
        else:
            print("Not enough money to invest in research & development.")
            bankruptcy()
    elif choice == '4':
        print("Chose not to invest this month.")
    else:
        print("Invalid choice.")
        bankruptcy()

def third_decision(assets):
    print("Decision 3: Harvesting Strategy")
    print("1. Harvest mushrooms yourself (Lower cost, less profit)")
    print("2. Hire workers to harvest ($3,000)")
    print("3. Use equipment for automated harvesting")
    print("4. Delay harvesting (Risk of spoilage)")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        print("You chose to harvest mushrooms yourself.")
        profit = harvest(assets, labor_cost=0, efficiency=1.0)
        assets['Money'] += profit
    elif choice == '2':
        if assets['Money'] >= 3000:
            print("You hired workers to harvest mushrooms.")
            assets['Money'] -= 3000
            profit = harvest(assets, labor_cost=3000, efficiency=1.5)
            assets['Money'] += profit
        else:
            print("Not enough money to hire workers.")
            bankruptcy()
    elif choice == '3':
        equipment_cost = 2000
        if assets['Money'] >= equipment_cost and assets['Equipment'] > 0:
            print("You used automated equipment for harvesting.")
            assets['Money'] -= equipment_cost
            profit = harvest(assets, labor_cost=1000, efficiency=2.0)
            assets['Money'] += profit
        else:
            print("Not enough money or equipment to use automated harvesting.")
            bankruptcy()
    elif choice == '4':
        print("You chose to delay harvesting. Mushrooms may spoil.")
        spoil_chance = 0.5
        if random.random() < spoil_chance:
            print("Oh no! Your mushrooms spoiled.")
            assets['Mushrooms'] = 0
        else:
            print("Fortunately, your mushrooms did not spoil.")
            profit = harvest(assets, labor_cost=0, efficiency=1.0)
            assets['Money'] += profit
    else:
        print("Invalid choice.")
        bankruptcy()

def harvest(assets, labor_cost, efficiency=1.0):
    # Calculate mushrooms harvested based on land and equipment
    base_yield = assets['Land'] * 200  # 200 mushrooms per acre
    equipment_bonus = assets['Equipment'] * 50  # Additional mushrooms per equipment unit
    staff_bonus = assets['Staff'] * 30       # Additional mushrooms per staff
    research_bonus = assets['Research'] * 20  # Bonus from R&D

    total_mushrooms = base_yield + equipment_bonus + staff_bonus + research_bonus
    total_mushrooms = int(total_mushrooms * efficiency)

    # Apply marketing boost if applicable
    if assets['Marketing']:
        total_mushrooms = int(total_mushrooms * 1.2)  # 20% increase
        print("Marketing boost applied! Increased mushroom sales by 20%.")
        assets['Marketing'] = False  # Reset marketing flag

    print(f"Harvested {total_mushrooms} mushrooms.")
    assets['Mushrooms'] += total_mushrooms

    # Calculate profit
    price_per_mushroom = 10  # Base price
    profit = assets['Mushrooms'] * price_per_mushroom - labor_cost
    print(f"Profit from harvest: ${profit}")
    assets['Mushrooms'] = 0  # Reset stock after harvesting
    return profit

def fourth_decision(assets):
    print("Decision 4: Business Strategy")
    print("1. Expand by purchasing more land and equipment")
    print("2. Consolidate and improve current operations")
    print("3. Take a loan to boost your business ($5,000)")
    print("4. Save money for future investments")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        print("Choosing to expand your business.")
        acres = input("How many additional acres would you like to buy? ($5,000 per acre): ")
        units = input("How many additional equipment units would you like to buy? ($3,000 per unit): ")
        if acres.isdigit() and int(acres) >= 0 and units.isdigit() and int(units) >= 0:
            cost = 5000 * int(acres) + 3000 * int(units)
            if assets['Money'] >= cost:
                assets['Land'] += int(acres)
                assets['Equipment'] += int(units)
                assets['Money'] -= cost
                print(f"Purchased {acres} acre(s) and {units} equipment unit(s).")
            else:
                print("Not enough money to expand.")
                bankruptcy()
        else:
            print("Invalid input. Must enter non-negative numbers.")
            bankruptcy()
    elif choice == '2':
        print("Choosing to consolidate and improve operations.")
        upgrade_cost = 2000
        if assets['Equipment'] > 0 and assets['Money'] >= upgrade_cost:
            assets['Equipment'] += 1  # Upgrade equipment
            assets['Money'] -= upgrade_cost
            print("Upgraded equipment. Increased harvesting efficiency.")
        else:
            print("Cannot upgrade equipment. Either no equipment or insufficient funds.")
            bankruptcy()
    elif choice == '3':
        print("Taking a loan of $5,000 with 10% interest.")
        assets['Money'] += 5000
        assets['Debt'] += 5000
    elif choice == '4':
        print("Choosing to save money for future investments.")
    else:
        print("Invalid choice.")
        bankruptcy()

def random_event(assets):
    print("\n--- Random Event ---")
    event_chance = random.random()
    if event_chance < 0.3:
        # Positive event
        positive_events = [
            "You received a bulk order from a local supermarket!",
            "A competitor went out of business, increasing your market share.",
            "A government grant for sustainable farming practices was awarded to you."
        ]
        event = random.choice(positive_events)
        print(f"Good News: {event}")
        assets['Money'] += 3000
    elif event_chance < 0.6:
        # Negative event
        negative_events = [
            "A sudden frost damaged some of your crops.",
            "A pest infestation has reduced your mushroom yield.",
            "Unexpected equipment failure caused delays in harvesting."
        ]
        event = random.choice(negative_events)
        print(f"Bad News: {event}")
        assets['Money'] -= 3000
    else:
        # No event
        print("No significant events this month.")
    print("----------------------\n")

def financial_update(assets):
    print("=== Financial Update ===")
    # Interest on debt
    if assets['Debt'] > 0:
        interest = assets['Debt'] * 0.10  # 10% interest
        print(f"Interest on debt: ${interest:.2f}")
        assets['Money'] -= interest

    # Monthly expenses for staff
    staff_expenses = assets['Staff'] * 1000  # $1,000 per staff member
    if staff_expenses > 0:
        print(f"Staff expenses: ${staff_expenses}")
        assets['Money'] -= staff_expenses

    # Monthly maintenance for equipment
    equipment_expenses = assets['Equipment'] * 500  # $500 per equipment unit
    if equipment_expenses > 0:
        print(f"Equipment maintenance expenses: ${equipment_expenses}")
        assets['Money'] -= equipment_expenses

    print("-------------------------\n")

def check_game_status(assets):
    if assets['Money'] < 0:
        bankruptcy()
    elif assets['Month'] > 12:
        victory(assets)
    elif assets['Debt'] > 20000:
        print("Your debt has exceeded $20,000. You cannot manage your loans anymore.")
        bankruptcy()

def victory(assets):
    print("\n==========================================")
    print("Congratulations! You've successfully managed your mushroom farming business for 12 months.")
    print("==========================================\n")
    print("Final Assets:")
    print_current_assets(assets)
    print("Thank you for playing! You built a sustainable mushroom farming empire!")
    sys.exit()

def bankruptcy():
    print("\n==========================================")
    print("BANKRUPTCY")
    print("==========================================")
    print("Due to poor financial management or unforeseen events, you've gone bankrupt.")
    print("Game Over.")
    sys.exit()

if __name__ == "__main__":
    start_game()
