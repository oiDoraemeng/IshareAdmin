
def xss_escape(s: str):
    '''
    对可能导致xss攻击的特殊字符进行转义
    :param s:
    :return:
    '''
    if s is None:
        return None
    else:
        return s.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;").replace("'", "&#39;").replace('"',
                                                                                                               "&#34;")


def regConvert(s):
    '''
    正则表达式特殊字符转义
    :param s:
    :return:
    '''
    a = {"&": "&amp;",
         ">": "&gt;",
         "<": "&lt;",
         "'": "&#39;",
         '"': "&#34;",
         '$': "\\$",
         '(': "\\(",
         ')': "\\)",
         ",": "\\,",
         "*": "\\*",
         "+": "\\+",
         ".": "\\.",
         "[": "\\[.",
         "]": "\\]",
         "?": "\\?",
         "\\": "\\\\",
         "^": "\\^",
         "{": "\\{",
         "}": "\\}",
         "|": "\\|"}
    ret=""
    if s is None:
        return None
    for x in s:
        if a.get(x) is None:
            ret+=x
        else:
            ret+= a.get(x)
    return ret
    
