import cx_Oracle 

from rqalpha.interface import AbstractMod
from .windportal import WindPortal

#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class WindMod(AbstractMod):
    def __init__(self):
        import os
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
        pass

    def start_up(self, env, mod_config):
        self.connection = cx_Oracle.connect(mod_config.wind_id,
                                            mod_config.wind_password, 
                                            mod_config.wind_address)
        env.set_data_source(WindPortal(env.config.base.data_bundle_path,
                                            {},
                                            self.connection)
                            )

    def tear_down(self, code, exception=None):
        self.connection.close()
        pass