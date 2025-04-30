from GUI import ct, base_classes


class Widgets(base_classes.TabStarter):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        ct.Button(self.container,
                  text='SQL to Files',
                  command=self.try_it)

    def try_it(self, *args, **kwargs):
        print("Tried. Succeeded.")