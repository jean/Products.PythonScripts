##############################################################################
# 
# Zope Public License (ZPL) Version 1.0
# -------------------------------------
# 
# Copyright (c) Digital Creations.  All rights reserved.
# 
# This license has been certified as Open Source(tm).
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions in source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 
# 3. Digital Creations requests that attribution be given to Zope
#    in any manner possible. Zope includes a "Powered by Zope"
#    button that is installed by default. While it is not a license
#    violation to remove this button, it is requested that the
#    attribution remain. A significant investment has been put
#    into Zope, and this effort will continue if the Zope community
#    continues to grow. This is one way to assure that growth.
# 
# 4. All advertising materials and documentation mentioning
#    features derived from or use of this software must display
#    the following acknowledgement:
# 
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
# 
#    In the event that the product being advertised includes an
#    intact Zope distribution (with copyright and license included)
#    then this clause is waived.
# 
# 5. Names associated with Zope or Digital Creations must not be used to
#    endorse or promote products derived from this software without
#    prior written permission from Digital Creations.
# 
# 6. Modified redistributions of any form whatsoever must retain
#    the following acknowledgment:
# 
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
# 
#    Intact (re-)distributions of any official Zope release do not
#    require an external acknowledgement.
# 
# 7. Modifications are encouraged but must be packaged separately as
#    patches to official Zope releases.  Distributions that do not
#    clearly separate the patches from the original work must be clearly
#    labeled as unofficial distributions.  Modifications which do not
#    carry the name Zope may be packaged in any form, as long as they
#    conform to all of the clauses above.
# 
# 
# Disclaimer
# 
#   THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS ``AS IS'' AND ANY
#   EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL CREATIONS OR ITS
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
#   USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#   OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#   SUCH DAMAGE.
# 
# 
# This software consists of contributions made by Digital Creations and
# many individuals on behalf of Digital Creations.  Specific
# attributions are listed in the accompanying credits file.
# 
##############################################################################
import sys

try:
    sys.path.insert(0, '.')
    import ZODB
except:
    sys.path.insert(0, '../../..')
    import ZODB

from Products.PythonScripts.PythonScript import PythonScript
from AccessControl.SecurityManagement import newSecurityManager

newSecurityManager(None, None)

from unittest import TestCase, TestSuite, VerboseTextTestRunner, makeSuite

TextTestRunner = VerboseTextTestRunner

# Test Classes

def readf(name):
    return open('tscripts/%s%s' % (name, '.ps'), 'r').read()

class TestPythonScriptNoAq(TestCase):
    def _newPS(self, txt):
        ps = PythonScript('ps')
        ps.ZBindings_edit({})
        ps.write(txt)
        ps._makeFunction(1)
        return ps

    def testEmpty(self):
        empty = self._newPS('')()
        assert empty is None, empty

    def testReturn(self):
        return1 = self._newPS('return 1')()
        assert return1 == 1, return1

    def testReturnNone(self):
        none = self._newPS('return')()
        assert none == None

    def testParam1(self):
        txt = self._newPS('##parameters=x\nreturn x')('txt')
        assert txt == 'txt', txt

    def testParam2(self):
       one, two = self._newPS('##parameters=x,y\nreturn x,y')('one','two')
       assert one == 'one'
       assert two == 'two'

    def testParam26(self):
        import string
        params = string.letters[:26]
        sparams = string.join(params, ',')
        tup = apply(self._newPS('##parameters=%s\nreturn %s'
                                % (sparams,sparams)), params)
        assert tup == tuple(params), (tup, params)
        
    def testArithmetic(self):
        one = self._newPS('return 1 * 5 + 4 / 2 - 6')()
        assert one == 1, one

    def testImport(self):
        a,b,c = self._newPS('import string; return string.split("a b c")')()
        assert a == 'a'
        assert b == 'b'
        assert c == 'c'

    def testWhileLoop(self):
        one = self._newPS(readf('while_loop'))()
        assert one == 1

    def testForLoop(self):
        ten = self._newPS(readf('for_loop'))()
        assert ten == 10
        
    def testMutateLiterals(self):
        l, d = self._newPS(readf('mutate_literals'))()
        assert l == [2], l
        assert d == {'b': 2}

    def testTupleUnpackAssignment(self):
        d, x = self._newPS(readf('tuple_unpack_assignment'))()
        assert d == {'a': 0, 'b': 1, 'c': 2}, d
        assert x == 3, x

    def testDoubleNegation(self):
        one = self._newPS('return not not "this"')()
        assert one == 1

    def testTryExcept(self):
        a,b = self._newPS(readf('try_except'))()
        assert a==1
        assert b==1
        
    def testBigBoolean(self):
        true = self._newPS(readf('big_boolean'))()
        assert true, true

    def testFibonacci(self):
        r = self._newPS(readf('fibonacci'))()
        assert r == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377,
                     610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657,
                     46368, 75025, 121393, 196418, 317811, 514229, 832040,
                     1346269, 2178309, 3524578, 5702887, 9227465, 14930352,
                     24157817, 39088169, 63245986], r

test_classes = (TestPythonScriptNoAq,)

# unit test machinery

def test_suite():
    ts = []
    for tclass in test_classes:
        ts.append(makeSuite(tclass, 'test'))
    
    return TestSuite(tuple(ts))

def main():
    alltests=test_suite()
    runner = TextTestRunner()
    runner.run(alltests)

def debug():
   test_suite().debug()
    
if __name__=='__main__':
   if len(sys.argv) > 1:
      globals()[sys.argv[1]]()
   else:
      main()

