# coding: utf-8
import os

from django.core.management.base import BaseCommand

from dext.common.utils import s11n
from dext.common.utils import jinja2
from dext.settings import settings

from the_tale.statistics.conf import statistics_settings
from the_tale.statistics.prototypes import RecordPrototype

from the_tale.statistics import models

from the_tale.statistics.metrics import registrations
from the_tale.statistics.metrics import lifetime
from the_tale.statistics.metrics import monetization
from the_tale.statistics.metrics import actual
from the_tale.statistics.metrics import forum
from the_tale.statistics.metrics import bills
from the_tale.statistics.metrics import folclor


METRICS = [
        registrations.RegistrationsCompleted,
        registrations.RegistrationsTries,
        registrations.RegistrationsCompletedPercents,

        registrations.RegistrationsCompletedInMonth,
        registrations.RegistrationsTriesInMonth,
        registrations.RegistrationsCompletedPercentsInMonth,

        registrations.AccountsTotal,

        registrations.Referrals,
        registrations.ReferralsTotal,
        registrations.ReferralsPercents,

        registrations.ReferralsInMonth,

        actual.Premiums,
        actual.InfinitPremiums,
        actual.PremiumPercents,
        actual.Active,
        actual.DAU,
        actual.MAU,

        actual.ActiveOlderDay,
        actual.ActiveOlderWeek,
        actual.ActiveOlderMonth,
        actual.ActiveOlder3Month,
        actual.ActiveOlder6Month,
        actual.ActiveOlderYear,

        lifetime.AliveAfterDay,
        lifetime.AliveAfterWeek,
        lifetime.AliveAfterMonth,
        lifetime.AliveAfter3Month,
        lifetime.AliveAfter6Month,
        lifetime.AliveAfterYear,
        lifetime.AliveAfter0,
        lifetime.Lifetime,
        lifetime.LifetimePercent,

        monetization.Payers,
        monetization.Income,
        monetization.PayersInMonth,
        monetization.IncomeInMonth,
        monetization.ARPPU,
        monetization.ARPU,
        monetization.ARPPUInMonth,
        monetization.ARPUInMonth,
        monetization.PU,
        monetization.PUPercents,
        monetization.IncomeTotal,
        monetization.DaysBeforePayment,
        monetization.ARPNUWeek,
        monetization.ARPNUMonth,
        monetization.ARPNU3Month,
        monetization.LTV,

        monetization.Revenue,

        monetization.IncomeFromForum,
        monetization.IncomeFromSilent,
        monetization.IncomeFromGuildMembers,
        monetization.IncomeFromSingles,

        monetization.IncomeFromForumPercents,
        monetization.IncomeFromSilentPercents,
        monetization.IncomeFromGuildMembersPercents,
        monetization.IncomeFromSinglesPercents,

        monetization.IncomeFromGoodsPremium,
        monetization.IncomeFromGoodsEnergy,
        monetization.IncomeFromGoodsChest,
        monetization.IncomeFromGoodsPeferences,
        monetization.IncomeFromGoodsPreferencesReset,
        monetization.IncomeFromGoodsHabits,
        monetization.IncomeFromGoodsAbilities,
        monetization.IncomeFromGoodsClans,
        monetization.IncomeFromGoodsMarketCommission,
        monetization.IncomeFromTransferMoneyCommission,

        monetization.IncomeFromGoodsPremiumPercents,
        monetization.IncomeFromGoodsEnergyPercents,
        monetization.IncomeFromGoodsChestPercents,
        monetization.IncomeFromGoodsPeferencesPercents,
        monetization.IncomeFromGoodsPreferencesResetPercents,
        monetization.IncomeFromGoodsHabitsPercents,
        monetization.IncomeFromGoodsAbilitiesPercents,
        monetization.IncomeFromGoodsClansPercents,
        monetization.IncomeFromGoodsMarketCommissionPercents,
        monetization.IncomeFromTransferMoneyCommissionPercents,

        monetization.IncomeGroup0_500,
        monetization.IncomeGroup500_1000,
        monetization.IncomeGroup1000_2500,
        monetization.IncomeGroup2500_10000,
        monetization.IncomeGroup10000,

        monetization.IncomeGroup0_500Percents,
        monetization.IncomeGroup500_1000Percents,
        monetization.IncomeGroup1000_2500Percents,
        monetization.IncomeGroup2500_10000Percents,
        monetization.IncomeGroup10000Percents,

        monetization.IncomeGroupIncome0_500,
        monetization.IncomeGroupIncome500_1000,
        monetization.IncomeGroupIncome1000_2500,
        monetization.IncomeGroupIncome2500_10000,
        monetization.IncomeGroupIncome10000,

        monetization.IncomeGroupIncome0_500Percents,
        monetization.IncomeGroupIncome500_1000Percents,
        monetization.IncomeGroupIncome1000_2500Percents,
        monetization.IncomeGroupIncome2500_10000Percents,
        monetization.IncomeGroupIncome10000Percents,

        forum.Posts,
        forum.PostsInMonth,
        forum.PostsTotal,
        forum.Threads,
        forum.ThreadsInMonth,
        forum.ThreadsTotal,
        forum.PostsPerThreadInMonth,

        bills.Bills,
        bills.BillsInMonth,
        bills.BillsTotal,
        bills.Votes,
        bills.VotesInMonth,
        bills.VotesTotal,
        bills.VotesPerBillInMonth,

        folclor.Posts,
        folclor.PostsInMonth,
        folclor.PostsTotal,
        folclor.Votes,
        folclor.VotesInMonth,
        folclor.VotesTotal,
        folclor.VotesPerPostInMonth
    ]


class Command(BaseCommand):

    help = 'complete statistics'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-f', '--force-clear', action='store_true', dest='force-clear', help='force clear all metrics')
        parser.add_argument('-l', '--log', action='store_true', dest='verbose', help='print log')
        parser.add_argument('-r', '--recalculate-last', action='store_true', dest='recalculate-last', help='recalculate last day')

    def handle(self, *args, **options):

        force_clear = options.get('force-clear')
        verbose = options.get('verbose')
        recalculate = options.get('recalculate-last')

        if recalculate:
            for MetricClass in METRICS:
                RecordPrototype._db_filter(date=MetricClass._last_datetime().date(),
                                           type=MetricClass.TYPE).delete()

        for MetricClass in METRICS:
            if force_clear or MetricClass.FULL_CLEAR_RECUIRED:
                if verbose:
                    print('clear %s' % MetricClass.TYPE)
                MetricClass.clear()

        for i, MetricClass in enumerate(METRICS):
            metric = MetricClass()
            if verbose:
                print('[%3d] calculate %s' % (i, metric.TYPE))

            metric.initialize()
            metric.complete_values()

        models.FullStatistics.objects.all().delete()
        models.FullStatistics.objects.create(data=RecordPrototype.get_js_data())
