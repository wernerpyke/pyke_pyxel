import pytest
from unittest.mock import patch, MagicMock

from pyke_pyxel.math import RandomChoice, WeightedChoice


class TestRandomChoiceCreation:
    """Tests for RandomChoice creation and initialization."""

    def test_basic_creation(self):
        choices = ["A", "B", "C"]
        rc = RandomChoice(choices)
        assert rc is not None

    def test_creation_with_empty_list(self):
        rc = RandomChoice([])
        assert rc is not None

    def test_creation_with_single_item(self):
        rc = RandomChoice(["only_one"])
        assert rc is not None


class TestRandomChoiceSelectOne:
    """Tests for RandomChoice.select_one() method."""

    def test_select_one_returns_item_from_choices(self):
        choices = ["A", "B", "C"]
        rc = RandomChoice(choices)
        result = rc.select_one()
        assert result in choices

    def test_select_one_with_single_item(self):
        rc = RandomChoice(["only_one"])
        result = rc.select_one()
        assert result == "only_one"

    @patch('pyke_pyxel.math.random')
    def test_select_one_uses_random_choice(self, mock_random):
        mock_random.choice.return_value = "B"
        choices = ["A", "B", "C"]
        rc = RandomChoice(choices)
        result = rc.select_one()

        mock_random.choice.assert_called_once_with(choices)
        assert result == "B"

    def test_select_one_with_integers(self):
        choices = [1, 2, 3, 4, 5]
        rc = RandomChoice(choices)
        result = rc.select_one()
        assert result in choices

    def test_select_one_with_mixed_types(self):
        choices = [1, "two", 3.0, None]
        rc = RandomChoice(choices)
        result = rc.select_one()
        assert result in choices


class TestWeightedChoiceCreation:
    """Tests for WeightedChoice creation and initialization."""

    def test_basic_creation(self):
        wc = WeightedChoice()
        assert wc is not None

    def test_creation_starts_empty(self):
        wc = WeightedChoice()
        assert len(wc._population) == 0
        assert len(wc._weights) == 0


class TestWeightedChoiceSet:
    """Tests for WeightedChoice.set() method."""

    def test_set_choices_and_probabilities(self):
        wc = WeightedChoice()
        choices = ["A", "B", "C"]
        probabilities = [0.3, 0.4, 0.3]
        wc.set(choices, probabilities)

        assert wc._population == choices
        assert wc._weights == probabilities

    def test_set_replaces_previous_values(self):
        wc = WeightedChoice()
        wc.set(["X", "Y"], [0.5, 0.5])
        wc.set(["A", "B", "C"], [0.3, 0.4, 0.3])

        assert wc._population == ["A", "B", "C"]
        assert wc._weights == [0.3, 0.4, 0.3]


class TestWeightedChoiceAdd:
    """Tests for WeightedChoice.add() method."""

    def test_add_single_choice(self):
        wc = WeightedChoice()
        wc.add("A", 0.5)

        assert "A" in wc._population
        assert 0.5 in wc._weights

    def test_add_multiple_choices(self):
        wc = WeightedChoice()
        wc.add("A", 0.3)
        wc.add("B", 0.4)
        wc.add("C", 0.3)

        assert wc._population == ["A", "B", "C"]
        assert wc._weights == [0.3, 0.4, 0.3]

    def test_add_appends_to_existing(self):
        wc = WeightedChoice()
        wc.set(["A", "B"], [0.4, 0.4])
        wc.add("C", 0.2)

        assert wc._population == ["A", "B", "C"]
        assert wc._weights == [0.4, 0.4, 0.2]


class TestWeightedChoiceReset:
    """Tests for WeightedChoice.reset() method."""

    def test_reset_clears_all(self):
        wc = WeightedChoice()
        wc.set(["A", "B", "C"], [0.3, 0.4, 0.3])
        wc.reset()

        assert len(wc._population) == 0
        assert len(wc._weights) == 0

    def test_reset_on_empty_is_noop(self):
        wc = WeightedChoice()
        wc.reset()  # Should not raise
        assert len(wc._population) == 0


class TestWeightedChoiceSelectOne:
    """Tests for WeightedChoice.select_one() method."""

    def test_select_one_returns_item_from_population(self):
        wc = WeightedChoice()
        wc.set(["A", "B", "C"], [0.3, 0.4, 0.3])
        result = wc.select_one()
        assert result in ["A", "B", "C"]

    def test_select_one_with_single_item(self):
        wc = WeightedChoice()
        wc.add("only_one", 1.0)
        result = wc.select_one()
        assert result == "only_one"

    @patch('pyke_pyxel.math.random')
    def test_select_one_uses_random_choices(self, mock_random):
        mock_random.choices.return_value = ["B"]
        wc = WeightedChoice()
        wc.set(["A", "B", "C"], [0.3, 0.4, 0.3])
        result = wc.select_one()

        mock_random.choices.assert_called_once_with(
            population=["A", "B", "C"],
            weights=[0.3, 0.4, 0.3],
            k=1
        )
        assert result == "B"

    def test_select_one_with_zero_weight(self):
        wc = WeightedChoice()
        # One item has zero weight - should never be selected
        wc.set(["A", "B"], [1.0, 0.0])

        # Run multiple selections - B should never appear
        for _ in range(50):
            result = wc.select_one()
            assert result == "A"

    def test_select_one_with_high_weight_dominates(self):
        wc = WeightedChoice()
        # Give A very high weight relative to others
        wc.set(["A", "B", "C"], [0.98, 0.01, 0.01])

        # Run multiple selections - A should appear most often
        results = [wc.select_one() for _ in range(100)]
        a_count = results.count("A")

        # A should appear in the vast majority of selections
        assert a_count >= 80


class TestWeightedChoiceEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_select_with_unnormalized_weights(self):
        wc = WeightedChoice()
        # Weights don't sum to 1.0 - should still work
        wc.set(["A", "B"], [1, 2])
        result = wc.select_one()
        assert result in ["A", "B"]

    def test_select_with_integer_weights(self):
        wc = WeightedChoice()
        wc.set(["A", "B", "C"], [1, 2, 3])
        result = wc.select_one()
        assert result in ["A", "B", "C"]

    def test_population_with_various_types(self):
        wc = WeightedChoice()
        wc.set([1, "two", 3.0], [0.3, 0.3, 0.4])
        result = wc.select_one()
        assert result in [1, "two", 3.0]
