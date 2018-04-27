class Object:
    """
    Turns every value, e.g. a String into a Object
    """

    def __init__(self, val):
        """
        Set the objects value to val
        :param val: Value of the object
        """

        self.setValue(val)

    def setValue(self, val):
        """"
        Set the objects value to val
        :param val: Value of the object
        :return:
        """

        self.obj = val
