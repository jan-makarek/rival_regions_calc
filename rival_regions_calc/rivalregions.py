
"""
The RivalRegions class
"""


class Item():
    """Represents an item in Rival Regions"""

    id = None
    name = None

    def __init__(self, name):
        """Initialize Resource"""
        self.id = self.items.get(name, None)
        if self.id is not None:
            self.name = name


    items = {
        "oil": 2,
        "ore": 5,
        "gold": 6,
        "uranium": 11,
        "diamond": 15,
        "liquid oxygen": 21,
        "helium": 24,
    }


class WorkProduction():
    """Calculate work productivity based on parameters

    Sources:
    http://wiki.rivalregions.com/Work_formulas
    """

    # Input
    resource = None
    user_level = 0
    work_exp = 0
    factory_level = 0
    resource_max = 0
    department_bonus = 0
    nation_bonus = False
    wage_percentage = 100
    state_tax = 0

    # Calculated
    _withdrawn_points = 0
    _productivity = 0
    _wage = 0
    _tax = 0
    _factory_profit = 0


    def __init__(self, item):
        """Initialize WorkProduction"""
        if not isinstance(item, Item):
            raise TypeError
        self.resource = item


    def print_settings(self):
        """Print the settings"""
        print(
            "Resource:        %16s\n" % (self.resource.name) +
            "user_level:      %16s\n" % (self.user_level) +
            "work_exp:        %16s\n" % (self.work_exp) +
            "factory_level:   %16s\n" % (self.factory_level) +
            "resource_max:    %16s\n" % (self.resource_max) +
            "dep_bonus:       %16s\n" % (self.department_bonus) +
            "nation_bonus:    %16s\n" % (self.nation_bonus) +
            "wage_percentage: %16s\n" % (self.wage_percentage) +
            "state_tax:       %16s\n" % (self.state_tax)
            )


    def calc(self, var, energy=None):
        """Calculate value vased on energy and return"""
        return 10 / energy * var


    def productivity(self, energy=10):
        """Return productivity"""
        return self.calc(self._productivity, energy)


    def withdrawn_points(self, energy=10):
        """Return withdrawn points"""
        return self.calc(self._withdrawn_points, energy)


    def wage(self, energy=10):
        """Return wage"""
        return self.calc(self._wage, energy)


    def tax(self, energy=10):
        """Return tax"""
        return self.calc(self._tax, energy)


    def factory_profit(self, energy=10):
        """Calculate wage"""
        return self.calc(self._factory_profit, energy)


    def resource_koef(self):
        """Calculate coefficient for resource"""
        if self.resource.id == 2 or self.resource.id == 5:
            return self.resource_max * 0.65
        if self.resource.id == 6:
            return self.resource_max * 0.4
        if self.resource.id == 11 or self.resource.id == 16:
            return self.resource_max * 0.75
        if self.resource.id == 21 or self.resource.id == 24:
            return pow(self.resource_max * 2, 0.4)
        return 0


    def calculate(self):
        """Calculate productivity"""

        self._productivity = 20 * \
                pow(self.user_level, 0.8) * \
                pow(self.resource_koef() / 10, 0.8) * \
                pow(self.factory_level, 0.8) * \
                pow(self.work_exp / 10, 0.6)

        if self.nation_bonus:
            self._productivity = self._productivity * 1.2

        self._productivity = self._productivity * (1 + self.department_bonus / 100)

        if self.resource.id == 6:
            self._productivity = self._productivity * 4
        elif self.resource.id == 15:
            self._productivity = self._productivity / 1000
        elif self.resource.id == 21:
            self._productivity = self._productivity / 5
        elif self.resource.id == 24:
            self._productivity = self._productivity / 1000

        # Tax
        self._tax = self._productivity / 100 * self.state_tax
        self._wage = self._productivity - self._tax

        # Factory profit
        self._factory_profit = self._wage / 100 * (100 - self.wage_percentage)
        self._wage = self._wage - self._factory_profit

        # Withdrawn
        self._withdrawn_points = self._productivity / 40000000
