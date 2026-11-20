
from src.generators.dim_date import generate_dim_date


def test_date_dimension_has_365_records():
    df = generate_dim_date()
    assert len(df) == 365


def test_date_key_is_unique():
    df = generate_dim_date()
    assert df["date_key"].is_unique


def test_date_dimension_has_no_missing_values():
    df = generate_dim_date()
    assert not df.isnull().any().any()


def test_weekend_flag_is_correct():
    df = generate_dim_date()

    expected = df["full_date"].dt.day_of_week >= 5

    assert (df["is_weekend"] == expected).all()
