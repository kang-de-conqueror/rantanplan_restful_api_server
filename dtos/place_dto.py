class PlaceDTO:
    def __init__(self, id, name, address):
        self._id = id
        self._name = name
        self._address = address

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def address(self):
        return self._address

    @address.setter
    def id(self, address):
        self._address = address
