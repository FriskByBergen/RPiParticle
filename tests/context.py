from friskby import DeviceConfig


class TestContext(object):
    def __init__(self):
        self.post_key = "6c918af4-7ab0-4812-a73e-80f7ed4f10f9"
        self.device_id = "FriskPITest"
        self.server_url = "https://friskby.herokuapp.com"
        self.post_path = "sensor/api/device/%s/" % self.device_id

        self.device_config = DeviceConfig.download( "%s/%s" % (self.server_url , self.post_path) , post_key = self.post_key)
        self.sensor_id = "FriskPITest_PM10"

        self.device_config_broken = DeviceConfig.download( "%s/%s" % (self.server_url , self.post_path) , post_key = self.post_key)
        self.device_config_broken.data["server_url"] = "http://invalid.no"
