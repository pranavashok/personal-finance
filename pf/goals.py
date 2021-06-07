from datetime import datetime
from typing import List, Union

from dateutil.relativedelta import relativedelta


class Goal:
    """
    Class attributes:
        start_date (datetime) - date when the goal begins

        end_date (datetime) - date when the goal ends

        start_amount (float) - the initial lumpsum amount associated with the goal today

        inflation_rate (float or list of float) - expected inflation rate per annum, a single float
                    in case const inflation is assumed, else a list of inflation rates for each year
    """

    start_date: datetime
    end_date: datetime
    n_months: int
    start_amount: float
    inflation_rate: Union[float, List[float]]

    def __init__(
        self,
        start_date: datetime = datetime.now(),
        end_date: datetime = None,
        n_months: int = None,
        start_amount: float = 0,
        inflation_rate: Union[float, List[float]] = 5,
    ):
        self.start_date = start_date
        if end_date:
            assert n_months is None
            relative_delta = relativedelta(end_date, start_date)
            self.n_months = relative_delta.years * 12 + relative_delta.months
        if n_months:
            assert start_date is not None
            assert end_date is None
            self.n_months = n_months
        self.start_amount = start_amount
        self.inflation_rate = inflation_rate


class MonthlyGoal(Goal):
    """
    Class attributes:
        monthly_amount (float) - monthly expenditure in today's currency value
    """

    monthly_amount: float

    def __init__(self, monthly_amount: float, **kwargs):
        super().__init__(**kwargs)
        self.monthly_amount = monthly_amount

    def get_monthly_need(self, month_idx: int = None, date: datetime = None):
        """
        Compute the need for a specific month. Only one of the parameters may be present.

        :param month_idx: index of the month in question from the start date of the goal
        :param date: an absolute date belonging to the month in question
        :return: amount of money needed for the requested month
        """
        assert (month_idx is None) ^ (date is None)  # exactly one of them must be defined

        if date:
            relative_delta = relativedelta(date, self.start_date)
            month_idx = relative_delta.years * 12 + relative_delta.months

        if month_idx > self.n_months:
            return 0

        year_idx = month_idx // 12

        return self.monthly_amount * (1 + self.inflation_rate / 100) ** year_idx


class LumpsumGoal(Goal):
    """
    Class attributes:
        end_amount (float) - required end amount in today's currency value
    """

    end_amount: float

    def __init__(self, end_amount: float, **kwargs):
        super().__init__(**kwargs)
        self.end_amount = end_amount

    def get_lumpsum_need(self):
        """
        Computes the lumpsum needed at the end of the goal period.

        :return: inflation-adjusted amount
        """

        return self.end_amount * (1 + self.inflation_rate / 100) ** (self.n_months // 12)

    def get_monthly_need(self, month_idx: int = None, date: datetime = None):
        """
        Compute the need for a specific month. Only one of the parameters may be present.

        :param month_idx: index of the month in question from the start date of the goal
        :param date: an absolute date belonging to the month in question
        :return: amount of money needed for the requested month
        """
        assert (month_idx is None) ^ (date is None)  # exactly one of them must be defined

        if date:
            relative_delta = relativedelta(date, self.start_date)
            month_idx = relative_delta.years * 12 + relative_delta.months

        if month_idx > self.n_months:
            return 0

        inflation_adjusted_end_amount = self.get_lumpsum_need()
        monthly_need = inflation_adjusted_end_amount / self.n_months
        return monthly_need


def calculate():
    emergency_goal = LumpsumGoal(start_amount=0, end_amount=700000, start_date=datetime.now(), n_months=2)
    for month_idx in range(emergency_goal.n_months):
        print(f"{month_idx}: {emergency_goal.get_monthly_need(month_idx=month_idx)}")


if __name__ == "__main__":
    calculate()
