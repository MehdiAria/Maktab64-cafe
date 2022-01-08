class CreateOrderError(Exception):
    """
    This Error would raise when the Order.__init__ get any invalid value
    """
    def __init__(self, field, data, msg=""):
        super().__init__(data, msg)
        self.data = data
        self.field = field
        self.msg = msg

    def __str__(self):
        return f"{self.field} can not get {self.data}!{self.msg}"
