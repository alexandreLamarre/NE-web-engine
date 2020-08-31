from Function import Function
import os

if __name__ == "__main__":
        start_time = os.times()[0]
        success = 0
        num_tests = 0

        ## ======================= Object tests ===============================
        ##
        ## Full Interpreter tests
        FAILED = []

        function = Function("f(xax,xax) = (xaxxax)")
        if str(function) == "NAME: f VARS: [xax] FUNCS [xax*xax]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (sin(2x),cos(x5))")
        if str(function) == "NAME: f VARS: [x] FUNCS [sin(2*x),cos(x*5)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x,y) = (sin(2xy5), xlog(2x))")
        if str(function) == "NAME: f VARS: [x,y] FUNCS [sin(2*x*y*5),x*log(2*x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(cat) = (cat^2floor(cat))")
        if str(function) == "NAME: f VARS: [cat] FUNCS [cat**2*floor(cat)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x,a) = (log(x)a)")
        if str(function) == "NAME: f VARS: [x,a] FUNCS [log(x)*a]":
                success+= 1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x,a) = (pixa2pi3)")
        if str(function) == "NAME: f VARS: [x,a] FUNCS [pi*x*a*2*pi*3]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(piad,a) = (pi2piapipiad)")
        if str(function) == "NAME: f VARS: [piad,a] FUNCS [pi*2*pia*pi*piad]":
                success+= 1
        else:
                FAILED.append(function)
        num_tests+=1##checking for 'a' as var splits up 'piad' as a var
        function = Function("f(pied,a) = (pi2piapipied)")
        if str(function) == "NAME: f VARS: [pied,a] FUNCS [pi*2*pi*a*pi*pied]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(pied, pie, pi, p) = (piedpiepip)")
        if str(function) == "NAME: f VARS: [pied,pie,pi,p] FUNCS [pied*pie*pi*p]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(randomcosvariable, randomsinvariable) = (randomcosvariablerandomsinvariable)")
        if str(function) == "NAME: f VARS: [randomcosvariable,randomsinvariable] FUNCS [randomcosvariable*randomsinvariable]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (cos(x)2acos(x)2)")
        if str(function) == "NAME: f VARS: [x] FUNCS [cos(x)*2*acos(x)*2]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1

        function = Function("f(x) = (2(x+1))")
        if str(function) == "NAME: f VARS: [x] FUNCS [2*(x+1)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(og) = (log(og))")
        if str(function) == "NAME: f VARS: [og] FUNCS [log(og)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(l)= (log(l))")
        if str(function) == "NAME: f VARS: [l] FUNCS [log(l)]":
                success+= 1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x,a) = (xacosh(x))")
        if str(function) == "NAME: f VARS: [x,a] FUNCS [x*acosh(x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (eerf(x))")
        if str(function) == "NAME: f VARS: [x] FUNCS [e*erf(x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (lgamma(x))")
        if str(function) == "NAME: f VARS: [x] FUNCS [lgamma(x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (ceil(x))")
        if str(function) == "NAME: f VARS: [x] FUNCS [ceil(x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (isqrt(x))")
        if str(function) == "NAME: f VARS: [x] FUNCS [isqrt(x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(ei) = (ceil(ei))")
        if str(function) == "NAME: f VARS: [ei] FUNCS [ceil(ei)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(ling) = (ceiling(ling))")
        if str(function) == "NAME: f VARS: [ling] FUNCS [ceiling(ling)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x,og) = (og(x))")
        if str(function) == "NAME: f VARS: [x,og] FUNCS [og*(x)]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        ## Constants
        function = Function("f(x) = (ex)")

        if str(function) == "NAME: f VARS: [x] FUNCS [e*x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        function = Function("f(x) = (pix)")
        if str(function) == "NAME: f VARS: [x] FUNCS [pi*x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1

        function = Function("f(x) = (taux)")
        if str(function) == "NAME: f VARS: [x] FUNCS [tau*x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        ##TODO this one returns an error, need to check right allowed char constants too

        function = Function("f(x,,,,) = (x)")
        if str(function) == "NAME: f VARS: [x] FUNCS [x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1

        ##==================== End of object tests =============================
        print("{}/{} tests were successful for Function Object interpreter".format(success,num_tests))
        end_time = os.times()[0]
        if FAILED:
                print("The following functions failed the tests:")
                for i in FAILED:
                        print("\t" + str(i))
        print("Tests for Function interpreter were completed in {} seconds.".format(end_time-start_time))