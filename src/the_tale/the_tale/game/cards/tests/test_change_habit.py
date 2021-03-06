# coding: utf-8

from the_tale.common.utils import testcase

from the_tale.game.logic_storage import LogicStorage
from the_tale.game.logic import create_test_map

from the_tale.game.cards import effects

from the_tale.game.postponed_tasks import ComplexChangeTask
from the_tale.game.relations import HABIT_TYPE
from the_tale.game.balance import constants as c

from the_tale.game.cards.tests.helpers import CardsTestMixin


class ChangeHabitTestMixin(CardsTestMixin):
    CARD = None

    def setUp(self):
        super(ChangeHabitTestMixin, self).setUp()

        create_test_map()

        self.account_1 = self.accounts_factory.create_account()

        self.storage = LogicStorage()
        self.storage.load_account_data(self.account_1)

        self.hero = self.storage.accounts_to_heroes[self.account_1.id]

        self.card = self.CARD()

    def habit_value(self):
        if self.card.HABIT.is_HONOR:
            return self.hero.habit_honor.raw_value

        if self.card.HABIT.is_PEACEFULNESS:
            return self.hero.habit_peacefulness.raw_value

    def test_use(self):
        self.hero.change_habits(HABIT_TYPE.HONOR, -c.HABITS_BORDER if self.CARD.POINTS > 0 else c.HABITS_BORDER)
        self.hero.change_habits(HABIT_TYPE.PEACEFULNESS, -c.HABITS_BORDER if self.CARD.POINTS > 0 else c.HABITS_BORDER)

        with self.check_delta(self.habit_value, self.CARD.POINTS):
            result, step, postsave_actions = self.card.use(**self.use_attributes(storage=self.storage, hero=self.hero))

        self.assertEqual((result, step, postsave_actions), (ComplexChangeTask.RESULT.SUCCESSED, ComplexChangeTask.STEP.SUCCESS, ()))

    def test_no_effect(self):
        self.hero.change_habits(HABIT_TYPE.HONOR, -c.HABITS_BORDER if self.CARD.POINTS < 0 else c.HABITS_BORDER)
        self.hero.change_habits(HABIT_TYPE.PEACEFULNESS, -c.HABITS_BORDER if self.CARD.POINTS < 0 else c.HABITS_BORDER)

        with self.check_not_changed(self.habit_value):
            result, step, postsave_actions = self.card.use(**self.use_attributes(storage=self.storage, hero=self.hero))

        self.assertEqual((result, step, postsave_actions), (ComplexChangeTask.RESULT.FAILED, ComplexChangeTask.STEP.ERROR, ()))


class ChangeHabitHonorPlusUncommonTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorPlusUncommon

class ChangeHabitHonorMinusUncommonTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorMinusUncommon

class ChangeHabitPeacefulnessPlusUncommonTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessPlusUncommon

class ChangeHabitPeacefulnessMinusUncommonTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessMinusUncommon

class ChangeHabitHonorPlusRareTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorPlusRare

class ChangeHabitHonorMinusRareTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorMinusRare

class ChangeHabitPeacefulnessPlusRareTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessPlusRare

class ChangeHabitPeacefulnessMinusRareTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessMinusRare

class ChangeHabitHonorPlusEpicTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorPlusEpic

class ChangeHabitHonorMinusEpicTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorMinusEpic

class ChangeHabitPeacefulnessPlusEpicTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessPlusEpic

class ChangeHabitPeacefulnessMinusEpicTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessMinusEpic

class ChangeHabitHonorPlusLegendaryTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorPlusLegendary

class ChangeHabitHonorMinusLegendaryTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitHonorMinusLegendary

class ChangeHabitPeacefulnessPlusLegendaryTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessPlusLegendary

class ChangeHabitPeacefulnessMinusLegendaryTests(ChangeHabitTestMixin, testcase.TestCase):
    CARD = effects.ChangeHabitPeacefulnessMinusLegendary
