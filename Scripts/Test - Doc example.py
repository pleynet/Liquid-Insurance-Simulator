from typing import Optional, List

from classFolder.AMMClass import AMM

number_of_outcomes: int = 2
liquidity: float = 1000
fee: float = 0.02
outcome_names: Optional[List[str]] = ["A", "B"]

amm_obj = AMM(number_of_outcomes, liquidity, fee, outcome_names)

print(amm_obj.get_prices())
print(amm_obj.shares)

shares: float = amm_obj.buy_shares(0, 300)
print(amm_obj.get_prices())
print(amm_obj.shares)
print(shares)



number_of_outcomes: int = 4
liquidity: float = 1000
fee: float = 0.02
outcome_names: Optional[List[str]] = ["A", "B", "C", "D"]

amm_obj = AMM(number_of_outcomes, liquidity, fee, outcome_names)

print(amm_obj.get_prices())
print(amm_obj.shares)

shares: float = amm_obj.buy_shares(0, 300)
print(amm_obj.get_prices())
print(amm_obj.shares)
print(shares)

