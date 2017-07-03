import ephem


class Sun:

    def __init__(self):
        self.data = []

        m = ephem.Mars('1970')
        print(ephem.constellation(m))
