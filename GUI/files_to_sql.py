from GUI import ct, base_classes


class Widgets(base_classes.TabStarter):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.widgets()

    def widgets(self, *args, **kwargs):
        ct.Button(self.container,
                  text='Files to SQL',
                  command=self.try_it)

    def try_it(self, *args, **kwargs):
        print("Tried. Succeeded.")