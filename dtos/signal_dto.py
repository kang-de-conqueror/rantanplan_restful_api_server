class SignalDTO:
    def __init__(self, bssid, ssid, frequency, signal_level, sample_count):
        self._bssid = bssid
        self._ssid = ssid
        self._frequency = frequency
        self._signal_level = signal_level
        self._sample_count = sample_count

    @property
    def bssid(self):
        return self._bssid

    @bssid.setter
    def bssid(self, bssid):
        self._bssid = bssid

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, ssid):
        self._ssid = ssid

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency

    @property
    def signal_level(self):
        return self._signal_level

    @frequency.setter
    def signal_level(self, signal_level):
        self._signal_level = signal_level

    @property
    def sample_count(self):
        return self._sample_count

    @frequency.setter
    def sample_count(self, sample_count):
        self._sample_count = sample_count