import sys
import re
import collections

class Unglobber(object):

    def __init__(self, string):
        self.string = string.rstrip()
        self.unglobbed = []

    def unglob(self):
        glob = r'\(([^\)]+)\)'
        res = re.match(r'\A([^(]*)' + glob + r'(.*)\Z', self.string)
        if res == None:
            # no glob patterns in string
            self.unglobbed = [re.sub(r'\s+', ' ', self.string)]
        else:
            prefix = res.group(1)
            globs = res.group(2).split('|')
            suffix = res.group(3)
            for choice in globs:
                self.unglobbed += Unglobber(prefix+choice+suffix).unglob()
        return self.unglobbed

def check_dups(ary):
    utterances = map(lambda elt: re.sub(r'^\S+\s+', '', elt), ary)
    return [x for x,count in collections.Counter(utterances).items() if count > 1]

out = []
with open(sys.argv[1]) as f:
    for line in f:
        if re.match(r'\A\s*\Z', line):
            out.write("\n")
            continue
        unglobber = Unglobber(line)
        unglobber.unglob()
        out += unglobber.unglobbed

# check for dups
dups = check_dups(out)
if not dups:
    sys.stdout.write("\n".join(out) + "\n")
else:
    sys.stderr.write("Error: Duplicate utterances:\n{}\n".format("\n".join(dups)))
