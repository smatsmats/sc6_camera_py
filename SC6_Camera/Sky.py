import ephem
import datetime

from SC6_Camera import Logger


class Sky():

    def __init__(self, config):

        l = Logger.Logger(config)
        self.logger = l.getLogger("Sky")

        self.dt = datetime.datetime.now()
        self.longitude = config['Sun']['Long']
        self.latitude = config['Sun']['Lat']

        self.hor_neutral = config['Sun']['AngleHorizon']
        self.hor_civil = config['Sun']['AngleCivil']
        self.hor_nautical = config['Sun']['AngleNautical']

        self.sky_message = "Sunrise / Sunset times:\n"

        self.load()

        self.logger.debug(self.sky_message)

    def load(self):

        sun = ephem.Sun()
        moon = ephem.Moon()

        (self.sunrise, self.sunset) = self.body_rise_set(sun, self.hor_neutral)
        self.sky_message += "Horizon sunrise: %s sunset: %s\n" % (
            self.sunrise, self.sunset)

        (self.civil_dawn, self.civil_dusk) = self.body_rise_set(
            sun, self.hor_civil)
        self.sky_message += "Civil sunrise: %s sunset: %s\n" % (
            self.civil_dawn, self.civil_dusk)

        (self.naut_dawn, self.naut_dusk) = self.body_rise_set(
            sun, self.hor_nautical)
        self.sky_message += "Nautical sunrise: %s sunset: %s\n" % (
            self.naut_dawn, self.naut_dusk)

        (self.moonrise, self.moonset) = self.body_rise_set(moon, 0)
        self.sky_message += "Moon rise: %s set: %s\n" % (
            self.moonrise, self.moonset)

        self.noon = datetime.datetime(self.dt.year, self.dt.month, self.dt.day, 12, 0, 0)
        self.sky_message += "Noon is: %s\n" % self.noon

    def body_rise_set(self, body, horizon=0):
        here = ephem.Observer()
        here.date = self.dt
        here.lat = self.latitude
        here.lon = self.longitude
        here.horizon = horizon

        body_rise = ephem.localtime(here.next_rising(body))
        body_rise = body_rise.replace(microsecond=0)
        body_set = ephem.localtime(here.next_setting(body))
        body_set = body_set.replace(microsecond=0)

        return(body_rise, body_set)

    def sky_message(self):
        return self.sky_message
