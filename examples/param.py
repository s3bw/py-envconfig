from envconfig import param


p = param.Bool(default="t")

print(p("NONE"))
