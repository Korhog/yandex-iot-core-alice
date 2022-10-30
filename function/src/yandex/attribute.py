class attribute:
    attributes_member_name = "__attributes__"

    def __call__(self, func):
        if (func.__dict__.__contains__(attribute.attributes_member_name)):
            func.__dict__[attribute.attributes_member_name].append(self)
        else:
            func.__setattr__(attribute.attributes_member_name, [self])
        return func  