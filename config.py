import tomllib


class Configurator:
    def grab_config(self, *args, **kwargs):
        with open('config.toml', 'rb') as f:
            config_data = tomllib.load(f)
        config_data['supported_extensions'] = config_data['database_extensions'] + config_data['spreadsheet_extensions']
        return config_data
