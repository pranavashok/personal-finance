from datetime import datetime, timedelta

from pf.goals import MonthlyGoal
from pf.goals import LumpsumGoal


def test_get_monthly_need_monthly_goal():
    inflation_rate = 5

    goal = MonthlyGoal(
        monthly_amount=100,
        start_date=datetime.now(),
        end_date=datetime(2023, 12, 1, 1),
        start_amount=0,
        inflation_rate=inflation_rate,
    )

    for month_idx in range(0, 12):
        assert goal.get_monthly_need(month_idx=month_idx) == 100

    for month_idx in range(12, 24):
        assert goal.get_monthly_need(month_idx=month_idx) == 105

    for month_idx in range(24, 30):
        assert goal.get_monthly_need(month_idx=month_idx) == 110.25

    for month_idx in range(30, 36):
        assert goal.get_monthly_need(month_idx=month_idx) == 0


def test_get_monthly_need_lumpsum_goal():
    inflation_rate = 5

    goal = LumpsumGoal(
        end_amount=100,
        start_date=datetime.now(),
        end_date=datetime(2023, 12, 1, 1),
        start_amount=0,
        inflation_rate=inflation_rate,
    )

    for month_idx in range(0, goal.n_months):
        assert goal.get_monthly_need(month_idx=month_idx) == 110.25 / goal.n_months


def test_n_months_and_end_date():
    n_months_goal = LumpsumGoal(start_amount=0, end_amount=700000, start_date=datetime.now(), n_months=2)
    end_date_goal = LumpsumGoal(start_amount=0, end_amount=700000, start_date=datetime.now(), end_date=datetime.now()+timedelta(days=75))

    assert end_date_goal.n_months == n_months_goal.n_months

    for month_idx in range(n_months_goal.n_months):
        assert n_months_goal.get_monthly_need(month_idx) == end_date_goal.get_monthly_need(month_idx)
