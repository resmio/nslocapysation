

def is_literal_string(strng):
    is_literal_objc_nsstring = strng[0:2] == '@"' and strng[-1] == '"'
    is_literal_swift_string = strng[0] == '"' and strng[-1] == '"'
    return is_literal_objc_nsstring or is_literal_swift_string
