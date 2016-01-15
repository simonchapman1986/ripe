

def make_shortener(limit):
    def to_short_string(item):
        string = str(item)
        if len(string) > limit:
            return string[:limit] + '...'
        return string
    return to_short_string


def to_string(self, max_length, *fields):
    shortener = make_shortener(max_length)
    class_name = self.__class__.__name__
    field_values = ",".join(map(shortener, fields))
    return "<{}:{}>".format(class_name, field_values)
