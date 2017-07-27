
class Node(object):

    def __init__(self, id, x=None, y=None, z=None):

        self.__id = id
        self.__x = x
        self.__y = y
        self.__z = z
        self.__u1 = None
        self.__u2 = None
        self.__u3 = None
        self.__temperature = None

    def __str__(self):
        return "node id: " + str(self.__id) + " x: " + str(self.__x) + \
                " y: " + str(self.__y) +  " z: " + str(self.__z) + "\n"

    def set_id(self, id):
        self.__id = id

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_z(self, z):
        self.__z = z

    def get_id(self):
        return self.__id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z

    def get_u1(self):
        return self.__u1

    def get_u2(self):
        return self.__u2

    def get_u3(self):
        return self.__u3

    def set_u1(self, u1):
        self.__u1 = u1

    def set_u2(self, u2):
        self.__u2 = u2

    def set_u3(self, u3):
        self.__u3 = u3

    def set_temperature(self, temperature):
        self.__temperature = temperature
    def get_temperature(self):
        return self.__temperature








