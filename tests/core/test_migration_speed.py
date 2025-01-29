from verfishd import migration_speed_with_demographic_noise


def test_calculate_speed_for_E_is_1_and_random_is_0(monkeypatch):
    monkeypatch.setattr("numpy.random.normal", lambda loc, scale: 0.0)
    assert round(migration_speed_with_demographic_noise(1.0), 5) == 0.90909, "The migration speed should be 1.0 for E=1.0"

def test_calculate_speed_for_E_is_half_and_random_is_half(monkeypatch):
    monkeypatch.setattr("numpy.random.normal", lambda loc, scale: 0.5)
    assert round(migration_speed_with_demographic_noise(0.5), 5) == 0.90909, "The migration speed should be 1.0 for E=1.0"

def test_calculate_speed_for_E_is_minus_half_and_rand_is_02(monkeypatch):
    monkeypatch.setattr("numpy.random.normal", lambda loc, scale: 0.2)
    assert round(migration_speed_with_demographic_noise(-0.5), 5) == -0.47368, "The migration speed should be 1.0 for E=1.0"
