import re
class SemVer:
    def __init__(self,major=0,minor=0,patch=0,pre=None,build=None):
        self.major=major;self.minor=minor;self.patch=patch;self.pre=pre;self.build=build
    @staticmethod
    def parse(s):
        m=re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-([\.\w]+))?(?:\+([\w\.]+))?$',s)
        if not m: raise ValueError(f"Invalid semver: {s}")
        return SemVer(int(m[1]),int(m[2]),int(m[3]),m[4],m[5])
    def __str__(self):
        s=f"{self.major}.{self.minor}.{self.patch}"
        if self.pre: s+=f"-{self.pre}"
        if self.build: s+=f"+{self.build}"
        return s
    def _tuple(self): return (self.major,self.minor,self.patch,0 if self.pre is None else -1,self.pre or '')
    def __lt__(self,o): return self._tuple()<o._tuple()
    def __eq__(self,o): return self._tuple()==o._tuple()
    def __le__(self,o): return self<o or self==o
    def bump_major(self): return SemVer(self.major+1,0,0)
    def bump_minor(self): return SemVer(self.major,self.minor+1,0)
    def bump_patch(self): return SemVer(self.major,self.minor,self.patch+1)
    def satisfies(self,constraint):
        if constraint.startswith('^'):
            v=SemVer.parse(constraint[1:])
            return self>=v and self.major==v.major
        if constraint.startswith('~'):
            v=SemVer.parse(constraint[1:])
            return self>=v and self.major==v.major and self.minor==v.minor
        return self==SemVer.parse(constraint)
if __name__=="__main__":
    v=SemVer.parse("1.2.3-beta.1+build.42")
    assert str(v)=="1.2.3-beta.1+build.42"
    assert v.major==1 and v.pre=="beta.1"
    assert SemVer.parse("1.0.0")<SemVer.parse("2.0.0")
    assert SemVer.parse("1.0.0-alpha")<SemVer.parse("1.0.0")
    assert SemVer.parse("1.2.3").satisfies("^1.0.0")
    assert not SemVer.parse("2.0.0").satisfies("^1.0.0")
    assert SemVer.parse("1.2.5").satisfies("~1.2.3")
    assert not SemVer.parse("1.3.0").satisfies("~1.2.3")
    print(f"SemVer: {v}, bump_minor={v.bump_minor()}")
    print("All tests passed!")
