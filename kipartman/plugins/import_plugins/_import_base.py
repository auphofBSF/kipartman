class KipartmanImporter:
    def __init__(self):
        pass

    def validate(self):
        classname = self.__class__.__name__
        print("Validating: ", classname)
        try:
            self.extension
            self.wildcard
            self.import
            return True
        except AttributeError as e:
            print("{} is invalid: {}".format(classname, str(e)))