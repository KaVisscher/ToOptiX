class PoissonRatio():

    def __init__(self, poisson_ratio=None, temperature=None):

        self.__poisson_ratio = poisson_ratio
        self.__temperature = temperature

    def __str__(self):
        return "PoissonRatio: " + str(self.__poisson_ratio) + \
            " Temperature: " + str(self.__temperature) + "\n"

    def set_poisson_ratio(self, poisson_ratio):
        self.__poisson_ratio = poisson_ratio

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature

    def get_poisson_ratio(self):
        return self.__poisson_ratio
