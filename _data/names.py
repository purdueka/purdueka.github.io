
def getter_setter_gen(name, type_):
    def getter(self):
        return getattr(self, "__" + name)
    def setter(self, value):
        if not isinstance(value, type_):
            raise TypeError(f"{name} attribute must be set to an instance of {type_}")
        setattr(self, "__" + name, value)
    return property(getter, setter)

def auto_type_check(cls):
    new_dct = {}
    for key, value in cls.__dict__.items():
        if isinstance(value, type):
            value = getter_setter_gen(key, value)
        new_dct[key] = value
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls)(cls.__name__, cls.__bases__, new_dct)

@auto_type_check
class Member(object):
  role = str
  role_us = str
  name = str
  name_us = str
  email = str
  major = str
  def __init__(self):
    self.role = ""
    self.role_us = ""
    self.name = ""
    self.name_us = ""
    self.email = ""
    self.major = ""
  def __str__(self) -> str:
    return f"{hex(id(self))} {self.role}, {self.role_us}, {self.name}, {self.name_us}, {self.email}, {self.major}"

def lTrimToken(s: str, tok: str) -> str:
  if tok not in s:
    return s
  s = s.split(tok)
  return s[-1].strip()

def rTrimToken(s: str, tok: str) -> str:
  if tok not in s:
    return s
  s = s.split(tok)
  return s[0].strip()

def ptag2member(line: str) -> Member:
  ret = Member()
  dat = line.split('>')
  cur = 0
  def pop() -> str:
    nonlocal cur
    cur += 1
    if cur < len(dat):
      return rTrimToken(dat[cur], '<')
    else:
      return " "

  tok = pop()
  ret.role = tok
  if '(' in tok:
    ret.role = rTrimToken(tok, '(')
    ret.role_us = rTrimToken(lTrimToken(tok, '('), ')')
  tok = pop()
  if tok and tok[0].isalpha():
    ret.role_us = tok
    tok = pop()
  name = tok or pop()
  ret.name = rTrimToken(name, '(')
  ret.name_us = rTrimToken(lTrimToken(name, '('), ')')
  tok = pop() or pop()
  ret.major = tok
  tok = pop() or pop()
  ret.email = tok
  return ret


def yaml(member: Member) -> str:
  return f'''- name: {member.name}
  name_us: {member.name_us}
  major: {member.major}
  email: {member.email}
  role: {member.role}
  role_us: {member.role_us}
  image: 2022/{member.name}.jpeg
'''
  

with open('./names', "r") as f:
  for line in f:
    m = ptag2member(line)
    print(yaml(m))