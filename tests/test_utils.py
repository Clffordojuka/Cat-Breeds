from catinfo.utils import find_breed_info, breed_summary

SAMPLE = [
    {"name": "Siamese", "origin": "Thailand", "temperament": "Active", "life_span": "8 - 12", "weight": {"imperial": "8 - 10"}, "description": "Friendly cat"},
    {"name": "Maine Coon", "origin": "United States", "temperament": "Gentle", "life_span": "10 - 13", "weight": {"imperial": "9 - 18"}, "description": "Large cat"},
]

def test_find_exact_match():
    res = find_breed_info("Siamese", SAMPLE)
    assert res is not None
    assert res["name"] == "Siamese"

def test_find_case_insensitive():
    res = find_breed_info("siamese", SAMPLE)
    assert res is not None
    assert res["name"] == "Siamese"

def test_find_partial():
    res = find_breed_info("maine", SAMPLE)
    assert res is not None
    assert res["name"] == "Maine Coon"

def test_summary_contains_fields():
    breed = SAMPLE[0]
    s = breed_summary(breed)
    assert "Origin: Thailand" in s
    assert "Weight (imperial)" in s
