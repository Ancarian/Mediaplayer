class StringRedactor:

    @staticmethod
    def to_concatenate(string, string2, value):
        if len(string) > value:
            string = string[:value] + string2
        else:
            while len(string) < value:
                string += " "
        return string

    @staticmethod
    def swap(string, first, second):
        if len(string) > first and len(string) > second:
            string[first],string[second] = string[second],string[first]
            return string
        return string
