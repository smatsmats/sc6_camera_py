import ephem
import datetime
import pytz
import pprint

from SC6_Camera import Logger


class Sky():

    def __init__(self, config):

        l = Logger.Logger(config)
        self.logger = l.getLogger("Sky")

        self.tz = pytz.timezone(config['General']['Timezone'])
        self.utctz = pytz.timezone('UTC')
        self.dt = datetime.datetime.now(self.tz)

        self.longitude = config['Sun']['Long']
        self.latitude = config['Sun']['Lat']

        self.horizon_neutral = config['Sun']['AngleHorizon']
        self.horizon_civil = config['Sun']['AngleCivil']
        self.horizon_nautical = config['Sun']['AngleNautical']
        self.horizon_astronomical = config['Sun']['AngleAstronomical']
        self.horizon_user = config['Sun']['AngleUser']

        self.sky_message = "Sunrise / Sunset times:\n"

        self.twilight_type = config['Sun']['TwilightType']
        twilight_options = (
            'Astronomical', 'Nautical', 'Civil', 'Horizon', 'User')
        if self.twilight_type not in twilight_options:
            print "TwilightType not set correctly"
            exit(1)
        selected_angle = "Angle" + self.twilight_type
        self.horizon_selected = config['Sun'][selected_angle]

        self.load()

        self.logger.debug(self.sky_message)

    def load(self):

        sun = ephem.Sun()
        moon = ephem.Moon()

        # we calculate all of these since it's fun to show the times
        (self.sunrise, self.sunset) = self.body_rise_set(
            sun, self.horizon_neutral)
        self.sky_message += "Horizon sunrise: %s sunset: %s\n" % (
            self.sunrise, self.sunset)

        (self.civil_dawn, self.civil_dusk) = self.body_rise_set(
            sun, self.horizon_civil)
        self.sky_message += "Civil sunrise: %s sunset: %s\n" % (
            self.civil_dawn, self.civil_dusk)

        (self.naut_dawn, self.naut_dusk) = self.body_rise_set(
            sun, self.horizon_nautical)
        self.sky_message += "Nautical sunrise: %s sunset: %s\n" % (
            self.naut_dawn, self.naut_dusk)

        (self.asto_dawn, self.asto_dusk) = self.body_rise_set(
            sun, self.horizon_astronomical)
        self.sky_message += "Astronomical sunrise: %s sunset: %s\n" % (
            self.asto_dawn, self.asto_dusk)

        (self.user_dawn, self.user_dusk) = self.body_rise_set(
            sun, self.horizon_user)
        self.sky_message += "User specified horizon sunrise: %s sunset: %s\n" % (
            self.user_dawn, self.user_dusk)

        (self.start_time, self.end_time) = self.body_rise_set(
            sun, self.horizon_selected)
        self.sky_message += "Well start the show: %s end time: %s\n" % (
            self.start_time, self.end_time)

        (self.moonrise, self.moonset) = self.body_rise_set(moon, 0)
        self.sky_message += "Moon rise: %s set: %s\n" % (
            self.moonrise, self.moonset)

        self.noon = datetime.datetime(
            self.dt.year, self.dt.month, self.dt.day, 12, 0, 0)
        self.sky_message += "Noon is: %s" % self.noon

    def body_rise_set(self, body, horizon=0):
        here = ephem.Observer()

        # set the time to mindnigbht to make sure we get 'next sunrise"
        d = datetime.datetime(
            self.dt.year, self.dt.month, self.dt.day, 0, 0, 0, 0, self.tz)
        # emphem wants it in UTC
        here.date = d.astimezone(self.utctz)

        here.lat = self.latitude
        here.lon = self.longitude
        here.horizon = horizon

        body_rise = ephem.localtime(here.next_rising(body))
        body_rise = body_rise.replace(microsecond=0, tzinfo=self.tz)
        body_set = ephem.localtime(here.next_setting(body))
        body_set = body_set.replace(microsecond=0, tzinfo=self.tz)

        return(body_rise, body_set)

    def sky_message(self):
        return self.sky_message

    def check4newday(self, dt):
        if dt.date() != self.dt.date():
            self.logger.debug("in check4newday, will load")
            self.load()

    def is_hour_after_dusk(self):
        self.dt = datetime.datetime.now(self.tz)
        self.check4newday(self.dt)
        up = self.start_time
        down = self.end_time + datetime.timedelta(hours=1)

        if self.dt >= up and self.dt <= down:
            return 1
        else:
            return 0

    def is_sun(self):
        self.dt = datetime.datetime.now(self.tz)
        self.check4newday(self.dt)

        if self.dt >= self.start_time and self.dt <= self.end_time:
            return 1
        else:
            return 0
