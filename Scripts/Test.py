from typing import Optional, List

from classFolder.AMMClass import AMM

number_of_outcomes: int = 2
liquidity: float = 100
fee: float = 0
outcome_names: Optional[List[str]] = ["No damage", "Damage"]
outcome_no_damage: int = 0
outcome_damage: int = 1

amm_obj = AMM(number_of_outcomes, liquidity, fee, outcome_names)

print(amm_obj.get_prices())

# We have to actor : insurer and insured

probability_no_damage: float = 0.9

amount_insurer: float = 250
insurer_shares_no_damage: float = 0
insurer_shares_no_damage += amm_obj.buy_shares(outcome_no_damage, amount_insurer)
print(amm_obj.get_prices())
print(insurer_shares_no_damage)

amount_insured: float = 10
insured_shares_damage : float = 0
insured_shares_damage += amm_obj.buy_shares(outcome_damage, amount_insured)
print(amm_obj.get_prices())
print(insured_shares_damage)

print("Insurer investment: ", amount_insurer)
print("Insurer gain if no damage: ", insurer_shares_no_damage)
print("Expected gain: ", probability_no_damage * insurer_shares_no_damage - amount_insurer)

print("Insured investment: ", amount_insured)
print("Insured gain if damage: ", insured_shares_damage)
print("Expected gain: ", (1 - probability_no_damage) * insured_shares_damage - amount_insured)



print("-------------------------------------")


number_of_outcomes: int = 2
liquidity: float = 10
fee: float = 0
outcome_names: Optional[List[str]] = ["No damage", "Damage"]
outcome_no_damage: int = 0
outcome_damage: int = 1

amm_obj = AMM(number_of_outcomes, liquidity, fee, outcome_names)

print(amm_obj.get_prices())

# We have to actor : insurer and insured

probability_no_damage: float = 0.9

amount_insurer: float = 90
insurer_shares_no_damage: float = 0
insurer_shares_no_damage += amm_obj.buy_shares(outcome_no_damage, amount_insurer)
print(amm_obj.get_prices())
print(insurer_shares_no_damage)

amount_insured: float = 10
insured_shares_damage : float = 0
insured_shares_damage += amm_obj.buy_shares(outcome_damage, amount_insured)
print(amm_obj.get_prices())
print(insured_shares_damage)

print("Insurer investment: ", amount_insurer)
print("Insurer gain if no damage: ", insurer_shares_no_damage)
print("Expected gain: ", probability_no_damage * insurer_shares_no_damage - amount_insurer)

print("Insured investment: ", amount_insured)
print("Insured gain if damage: ", insured_shares_damage)
print("Expected gain: ", (1 - probability_no_damage) * insured_shares_damage - amount_insured)


