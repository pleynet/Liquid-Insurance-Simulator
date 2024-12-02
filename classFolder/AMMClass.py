from typing import Optional, List


class AMM:
    """
    This class implement teh behaviour of the Market created via Automated Market Maker (AMM)
    It compute the price of the asset in the market given the amount of the asset in the market
    This is implemented using Polymarket function : Fixed Product Market Maker
    See https://help.polkamarkets.com/how-polkamarkets-works/automated-market-maker-(amm) and https://help.polkamarkets.com/how-polkamarkets-works/trading-and-price-calculation
    """

    shares_rounding: int = 3
    epsilon: float = 0.01

    def __init__(self, number_of_outcomes: int, liquidity: float, fee: float = 0, outcome_names: Optional[List[str]] = None):

        assert number_of_outcomes > 1, "Number of outcomes must be greater than 1"
        self.number_of_outcomes = number_of_outcomes

        #assert fee == 0, "Fee is not implemented yet"
        assert fee >= 0, "Fee must be positive"
        self.fee = fee

        assert liquidity > 0, "Liquidity must be greater than 0"
        self.liquidity: float = liquidity
        self.liquidity_powered: float = liquidity ** number_of_outcomes

        self.shares: List[float] = [self.liquidity] * self.number_of_outcomes
        #self.shares = self.round_shares(self.shares)
        self.shares = [round(share, self.shares_rounding) for share in self.shares]

        if outcome_names is not None:
            assert len(outcome_names) == number_of_outcomes, "Number of outcome names must be equal to number of outcomes"
            self.outcome_names = outcome_names
        else:
            self.outcome_names = [f"Outcome {i}" for i in range(number_of_outcomes)]

        self.price_weights_list: Optional[List[float]] = None



    # def round_shares(self):
    #     self.shares = [round(share, self.shares_rounding) for share in self.shares]
    #def round_shares(self, shares_list: List[float]) -> List[float]:
    #    return [round(share, self.shares_rounding) for share in shares_list]

    def buy_shares(self, outcome: int, amount: float) -> float:
        """
        Buy amount of shares of outcome, and return teh amount of shares aquired
        """
        assert outcome >= 0 and outcome < self.number_of_outcomes, "Outcome must be between 0 and number_of_outcomes"
        assert amount >= 0, "Amount must be positive"

        # We copy the shares list
        #tmp_shares: List[float] = self.shares.copy()

        net_amount: float = amount * (1 - self.fee)
        net_amount = round(net_amount, self.shares_rounding)

        tmp_shares: List[float] = [shares + net_amount for shares in self.shares]

        prod_share_other_outcomes = 1
        for i in range(self.number_of_outcomes):
            if i != outcome:
                prod_share_other_outcomes *= tmp_shares[i]

        share_outcome = self.liquidity_powered / prod_share_other_outcomes
        share_outcome = round(share_outcome, self.shares_rounding)

        tmp_shares_outcome_before = tmp_shares[outcome]
        tmp_shares[outcome] = share_outcome

        # Debug, we assert that the product of shares is equal to the liquidity
        recompute_liquidity: float = 1
        for share in tmp_shares:
            recompute_liquidity *= share
        assert abs(self.liquidity_powered - recompute_liquidity) < self.epsilon * self.liquidity_powered, "Liquidity is not conserved"

        acquired_shares: float = tmp_shares_outcome_before - share_outcome
        assert acquired_shares >= 0, "Acquired shares is negative"

        self.shares = tmp_shares
        self.price_weights_list: Optional[List[float]] = None

        return acquired_shares

    def get_prices_list(self, outcome: int) -> float:
        """
        Return the price of the outcome
        """
        assert outcome >= 0 and outcome < self.number_of_outcomes, "Outcome must be between 0 and number_of_outcomes"

        if self.price_weights_list is None:
            self.price_weights_list = [0] * self.number_of_outcomes
            for i in range(self.number_of_outcomes):
                outcome_price_weight = 1
                for j in range(self.number_of_outcomes):
                    if j != i:
                        outcome_price_weight *= self.shares[j]
                self.price_weights_list[i] = outcome_price_weight

        #sum_share_outcomes = 0
        #for i in range(self.number_of_outcomes):
        #    sum_share_outcomes += self.price_weights_list[i]
        sum_share_outcomes = sum(self.price_weights_list)

        price: float = self.price_weights_list[outcome] / sum_share_outcomes

        assert 0 < price < 1, "Price is not between 0 and 1"

        return price

    def get_prices(self) -> List[float]:
        """
        Return the price of the outcomes
        """
        result: List[float] = [self.get_prices_list(i) for i in range(self.number_of_outcomes)]

        # Debug: we assert that the sum of the prices is equal to 1
        assert abs(sum(result) - 1) < self.epsilon, "Sum of prices is not equal to 1"

        return result