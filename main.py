from GUI import main_app
import config


def main():
    conf = config.Configurator()
    app = main_app.MainApp(conf.grab_config())
    app.mainloop()


if __name__ == '__main__':
    main()
