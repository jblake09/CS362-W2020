import random
from collections import defaultdict
from unittest import TestCase
import testUtility
import Dominion


class TestCard(TestCase):

    def SetUp(self):
        # Get player names
        # player_names = ["Annie","*Ben","*Carla"]
        self.player_names = testUtility.GetPlayers()

        # number of curses and victory cards
        if len(self.player_names) > 2:
            self.nV = 12
        else:
            self.nV = 8
        self.nC = -10 + 10 * len(self.player_names)
        # Refactored Get boxs
        self.box = testUtility.GetBoxes(self.nV)
        # refactored supplu order
        self.supply_order = testUtility.SupplyOrder()

        # Pick 10 cards from box to be in the supply.
        self.boxlist = [k for k in self.box]
        random.shuffle(self.boxlist)
        self.random10 = self.boxlist[:10]
        self.supply = defaultdict(list, [(k, self.box[k]) for k in self.random10])

        # The supply always has these cards
        self.supply["Copper"] = [Dominion.Copper()] * (60 - len(self.player_names) * 7)
        self.supply["Silver"] = [Dominion.Silver()] * 40
        self.supply["Gold"] = [Dominion.Gold()] * 30
        self.supply["Estate"] = [Dominion.Estate()] * self.nV
        self.supply["Duchy"] = [Dominion.Duchy()] * self.nV
        self.supply["Province"] = [Dominion.Province()] * self.nV
        self.supply["Curse"] = [Dominion.Curse()] * self.nC

        # initialize the trash
        self.trash = []

        self.player = Dominion.Player('Annie')

    def test_init(self):
        self.SetUp()

        cost = 1
        buypower = 5

        card = Dominion.Coin_card(self.player.name, cost, buypower)

        self.assertEqual('Annie', card.name)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(cost, card.cost)
        self.assertEqual("coin", card.category)
        self.assertEqual(0, card.vpoints)

    def test_react(self):
        pass


class TestPlayer(TestCase):

    def test_stack(self):
        player = Dominion.Player('Annie')
        self.assertEqual(10, len(player.stack()))

        player.deck = [Dominion.Copper()] * 10 + [Dominion.Estate()] * 3
        self.assertEqual(18, len(player.stack()))


class TestActionCard(TestCase):

    def setUp(self):

        self.player_names = testUtility.GetPlayers()

        # number of curses and victory cards
        if len(self.player_names) > 2:
            self.nV = 12
        else:
            self.nV = 8
        self.nC = -10 + 10 * len(self.player_names)
        # Refactored Get boxs
        self.box = testUtility.GetBoxes(self.nV)
        # refactored supplu order
        self.supply_order = testUtility.SupplyOrder()

        # Pick 10 cards from box to be in the supply.
        self.boxlist = [k for k in self.box]
        random.shuffle(self.boxlist)
        self.random10 = self.boxlist[:10]
        self.supply = defaultdict(list, [(k, self.box[k]) for k in self.random10])

        # The supply always has these cards
        self.supply["Copper"] = [Dominion.Copper()] * (60 - len(self.player_names) * 7)
        self.supply["Silver"] = [Dominion.Silver()] * 40
        self.supply["Gold"] = [Dominion.Gold()] * 30
        self.supply["Estate"] = [Dominion.Estate()] * self.nV
        self.supply["Duchy"] = [Dominion.Duchy()] * self.nV
        self.supply["Province"] = [Dominion.Province()] * self.nV
        self.supply["Curse"] = [Dominion.Curse()] * self.nC

        # initialize the trash
        self.trash = []
        self.name = "Blueberry"
        self.actions = 3
        self.coins = 10

        self.player = Dominion.Player('Annie')
        self.player2 = Dominion.Player('Carla')

    def test_init(self):
        self.setUp()
        card = Dominion.Action_card(self.name, 0, self.actions, 0, 5, self.coins)
        self.assertEqual("Blueberry", card.name)
        self.assertEqual(0, card.cost)
        self.assertEqual(3, card.actions)
        self.assertEqual(0, card.cards)
        self.assertEqual(5, card.buys)
        self.assertEqual(10, card.coins)

    def test_use(self):
        self.setUp()
        # Test with feast card
        self.player.hand.insert(0, Dominion.Feast())
        testCard = Dominion.Feast()
        self.assertEqual(testCard.name, self.player.hand[0].name)
        Dominion.Action_card.use(self.player.hand[0], self.player, self.trash)
        self.assertEqual(testCard.name, self.player.played[0].name)
        self.assertEqual(5, len(self.player.hand))
        # test with madeup blueberry card
        card = Dominion.Action_card(self.name, 0, self.actions, 0, 5, self.coins)
        self.player.hand.insert(0, card)
        self.assertEqual(card.name, self.player.hand[0].name)
        Dominion.Action_card.use(self.player.hand[0], self.player, self.trash)
        self.assertEqual(card.name, self.player.played[1].name)
        self.assertEqual(5, len(self.player.hand))

    def test_augment(self):
        self.setUp()
        #add action card to player hand and test intital values
        card = Dominion.Action_card(self.name, 0, self.actions, 10, 5, self.coins)
        self.player.hand.insert(0, card)
        self.assertEqual(3, self.player.hand[0].actions)
        self.assertEqual(5, self.player.hand[0].buys)
        self.assertEqual(10, self.player.hand[0].coins)
        self.assertEqual(10, self.player.hand[0].cards)
        self.assertEqual(11, len(self.player.stack()))
        self.player.actions = 0
        self.player.buys = 0
        self.player.purse = 0
        Dominion.Action_card.augment(self.player.hand[0], self.player)
        self.assertEqual(3, self.player.actions)
        self.assertEqual(5, self.player.buys)
        self.assertEqual(10, self.player.purse)


class TestPlayer(TestCase):
    def test_action_balance(self):
        pass
    def test_calc_points(self):
        pass
    def test_draw(self):
        pass
    def test_card_summary(self):
        pass

class TestGameOver(TestCase):


    def setUp(self):
        # Get player names
        # player_names = ["Annie","*Ben","*Carla"]
        self.player_names = testUtility.GetPlayers()

        # number of curses and victory cards
        if len(self.player_names) > 2:
            self.nV = 12
        else:
            self.nV = 8
        self.nC = -10 + 10 * len(self.player_names)
        # Refactored Get boxs
        self.box = testUtility.GetBoxes(self.nV)
        # refactored supplu order
        self.supply_order = testUtility.SupplyOrder()

        # Pick 10 cards from box to be in the supply.

        self.supply = defaultdict(list)

        # The supply always has these cards
        self.supply["Copper"] = [Dominion.Copper()]
        self.supply["Silver"] = [Dominion.Silver()]
        self.supply["Gold"] = [Dominion.Gold()]
        self.supply["Estate"] = [Dominion.Estate()]
        self.supply["Duchy"] = [Dominion.Duchy()]
        self.supply["Province"] = [Dominion.Province()]
        self.supply["Curse"] = [Dominion.Curse()]

        # initialize the trash
        self.trash = []

        self.player = Dominion.Player('Annie')

    def test_gameOver(self):
        self.setUp()
        #Test returns false right away
        self.assertEqual(False, Dominion.gameover(self.supply))
        self.supply["Province"] = []
        #Remove Province card should end game
        self.assertEqual(True, Dominion.gameover(self.supply))
        #Add back in
        self.supply["Province"] = [Dominion.Province()]
        #force out to equal 2 should not end game
        self.supply["Duchy"] = []
        self.supply["Curse"] = []
        self.assertEqual(False, Dominion.gameover(self.supply))
        #force out to equal 3 should end game
        self.supply["Silver"] = []
        self.assertEqual(True, Dominion.gameover(self.supply))
       # for stack in self.supply:
       #     print(len(self.supply[stack]))









