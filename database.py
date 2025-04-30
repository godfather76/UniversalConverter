from GUI import base_classes as base
from GUI import ct


class CreateDB:
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, close_cmd=base.MainBase.go_back, *args, **kwargs)
        # self.title("Create Database from Files")
        # self.wid = 900
        # self.ht = 600
        # self.geometry(f'{self.wid}x{self.ht}')
        self.options = ('SQL Database',
                        'SQLite Database')
        self.widgets()

    def widgets(self):
        ct.Button(self,
                  text='Back',
                  command=lambda: self.go_back(ask=False))
        ct.Label(self,
                 text='Create New Database',
                 column=1,
                 columnspan=5)
        ct.OptionMenu(self,
                      values=self.options,
                      row=5)

