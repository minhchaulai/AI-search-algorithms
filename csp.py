from collections import OrderedDict

canada = OrderedDict(
    [("AB", ["BC", "NT", "SK"]),
    ("BC", ["AB", "NT", "YT"]),
    ("LB", ["NF", "NS", "PE", "QC"]),
    ("MB", ["ON", "NV", "SK"]),
    ("NB", ["NS", "QC"]),
    ("NF", ["LB", "QC"]),
    ("NS", ["LB", "NB", "PE"]),
    ("NT", ["AB", "BC", "NV", "SK", "YT"]),
    ("NV", ["MB", "NT"]),
    ("ON", ["MB", "QC"]),
    ("PE", ["LB", "NS", "QC"]),
    ("QC", ["LB", "NB", "NF", "ON", "PE"]),
    ("SK", ["AB", "MB", "NT"]),
    ("YT", ["BC", "NT"])])

states = ["AB", "BC", "LB", "MB", "NB", "NF", "NS", "NT", "NV", "ON", "PE", "QC", "SK", "YT"]
colors = ["blue", "green", "red"]


class CSP:
    def __init__(self, vars, neighbors, domain):
        self.variables = vars
        self.adjacent = neighbors
        self.assign = domain
    # your code here#


cspObj = CSP(states, canada, colors)

# print(cspObj.neighbors)
# print(cspObj.variables)
# print(cspObj.domain)
