from Function import Function
import os

if __name__ == "__main__":
        start_time = os.times()[0]
        success = 0
        num_tests = 0
        ### _PARSE_INPUT Tests
        ##################################### GENERAL METHODS TESTS #############################################

        ## Instantiation of FUnction object doesn't matter here, it will be reused to test a method
        FAILED = []
        function = Function("f(x) = (x)")

        test_string = "f(x) = (x)"
        res = function._parse_input(test_string)
        if res[0] == "f" and res[1] == ["x"] and res[2] == ["x"]:
            success+=1
        else:
            FAILED.append((test_string, res[0], res[1], res[2]))
        num_tests+=1

        test_string = "f(x,y) = (x^2y^2, x)"
        res = function._parse_input(test_string)
        if res[0] == "f" and res[1] == ["x","y"] and res[2] == ["x^2y^2", "x"]:
            success+=1
        else:
            FAILED.append((test_string, res[0], res[1], res[2]))
        num_tests+=1

        test_string = "function1name(varone, vartwo) = (varone, vartwo)"
        res = function._parse_input(test_string)
        if res[0] == "function1name" and res[1] == ["varone", "vartwo"] \
                                                and res[2] == ["varone", "vartwo"]:
            success+=1
        else:
            FAILED.append((test_string, res[0], res[1], res[2]))
        num_tests+=1

        test_string = "f(x) = ()"
        res = function._parse_input(test_string)
        if res[0] == "f" and res[1] == ["x"] and res[2] == []:
            success+=1
        else:
            FAILED.append((test_string, res[0], res[1], res[2]))
        num_tests += 1

        test_string = "functionname  (x,y,z,x) = (xyzyxyxyx)"

        res = function._parse_input(test_string)
        if res[0] == "functionname" and res[1] == ["x", "y", "z", "x"]\
                                                and res[2] == ["xyzyxyxyx"]:
            success+=1
        else:
            FAILED.append((test_string, res[0], res[1], res[2]))
        num_tests += 1

        test_string = "name(x,,,,,x) = (log(x),,,sin(x))"
        res = function._parse_input(test_string)
        if res[0] == "name" and res[1] == ["x", "x"] and res[2] == ["log(x)", "sin(x)"]:
                success+=1
        else:
                FAILED.append(test_string)
        num_tests += 1

        end_time = os.times()[0]
        print("{}/{} tests passed for _parse_input method".format(success, num_tests))
        if FAILED:
            print("The following strings failed the tests")
            for i in FAILED:
                for j in i:
                        print("\t" + str(j))

        print("Testing '_parse_input' method for Function took {} seconds.".format(end_time-start_time))
        print("\n")
        ## ===================== end _parse_input tests ==========================

        ## ======================== preprocess_variables tests =======================
        success = 0
        num_tests = 0
        FAILED = []
        ## placehold object to test preprocess_variables
        function = Function("f(x) = (x)")

        test_list = ["x"]
        res = function.preprocess_variables(test_list)
        if res == ["x"]:
                success+=1
        else:
                FAILED.append((test_list,res))

        num_tests += 1

        test_list = ["var", "var", "vari"]
        res = function.preprocess_variables(test_list)
        if res == ["var", "vari"]:
                success+=1
        else:
                FAILED.append((test_list,res))

        num_tests +=1

        test_list = ["x", "x"]
        res = function.preprocess_variables(test_list)
        if res == ["x"]:
                success+=1
        else:
                FAILED.append((test_list,res))

        num_tests += 1

        end_time = os.times()[0]
        print("{}/{} tests passed for preprocess_variables method".format(success, num_tests))
        if FAILED:
            print("The following variables list failed the test")
            for i in FAILED:
                    print("\t Expected: {}  Got: {}".format(i[0], i[1]))
        print("Testing preprocess_variables took {} seconds".format(end_time-start_time))
        print("\n")
        ## ======================== end of preprocess_variables tests ===============

        ## ==========================order_vars tests ==================================

        success = 0
        num_tests = 0
        FAILED = []

        ## placehold function to use order_var method
        function = Function("f(x) = (x)")

        test_var_list = ["x", "y", "z"]
        res = function.order_vars(test_var_list)
        if res == test_var_list:
                success+=1
        else:
                FAILED.append((test_var_list, res))
        num_tests +=1

        test_var_list = ["length", "lengt", "leng", "len"]
        res = function.order_vars(test_var_list)
        if res == test_var_list:
                success+=1
        else:
                FAILED.append((test_var_list, res))
        num_tests +=1

        ## next test is the list above in reverse order

        test_var_list = ["len", "leng", "lengt", "length"]
        res = function.order_vars(test_var_list)
        if res == ["length", "lengt", "leng", "len"]:
                success+=1
        else:
                FAILED.append((test_var_list,res))

        num_tests += 1
        ##next test is the list above in random order

        test_var_list = ["length","len", "leng", "lengt","leng", "len", "length"]
        res = function.order_vars(test_var_list)
        if res == ["length", "length", "lengt", "leng", "leng", "len", "len"]:
                success+=1
        else:
                FAILED.append((test_var_list,res))

        num_tests +=1

        end_time = os.times()[0]
        print("{}/{} tests passed for order_vars method".format(success, num_tests))
        if FAILED:
                print("The following failed the tests for order_vars:")
                for i in FAILED:
                        print("\t Expected: " + i[0] + " Got:  " + i[1])
        print("Testing order_vars method took {} seconds".format(end_time-start_time))
        print("\n")
        ## ========================= end of order_vars tests ===========================

        ## ========================= allowed_chars tests =================================

        success = 0
        num_tests = 0
        FAILED = []
        ## placeholder function for testing methods
        function = Function("f(x) = (x)")

        test_var = ""
        test_ordered_list = []
        res = function.allowed_chars(test_var, test_ordered_list)
        if res == "":
                success+=1
        else:
                FAILED.append(((test_var, test_ordered_list), res))

        num_tests +=1

        end_time = os.times()[0]
        print("{}/{} tests passed for allowed chars method.".format(success,num_tests))
        if FAILED:
                print("The following input (var, ordered_vars) failed the tests")
                for i in FAILED:
                        print("Input:"+ str(i[0][0]) + "," + str(i[0][1]) + " Got:  " + str(i[1]))
        print("Testing allowed_chars method took {} seconds".format(end_time-start_time))
        print("\n")
        ## ======================== end of allowed_chars tests ==============================

        ############################## END OF GENERAL METHODS TESTS ########################

        ############################# PREPROCESSES TESTS ################################

        ## ======================== preprocess_parentheses ==================================

        ## ======================== end of preprocess_parentheses =========================



        ############################# END PREPROCESSES TESTS #################################

        ## ======================= Things that should be interpreted tests ===============================
        success = 0
        num_tests = 0
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
        ## ==================== spaces that should be interpreted =============
        function = Function("f(x   ,   y) = (x x x, y   )")
        if str(function) == "NAME: f VARS: [x,y] FUNCS [x*x*x,y]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1

        function = Function("f (x,y)       =  (log    ( x   )    y)")

        if str(function) == "NAME: f VARS: [x,y] FUNCS [log(x)*y]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1
        ## ========================== Constants ==============================
        function = Function("f(x) = (ex)")

        if str(function) == "NAME: f VARS: [x] FUNCS [e*x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1

        function = Function("f(x) = (ex x)")
        if str(function) == "NAME: f VARS: [x] FUNCS [e*x*x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests +=1

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

        ## =========='Invalid' variables /functions that should be interpreted==========
        function = Function("f(x,,,,) = (x)")
        if str(function) == "NAME: f VARS: [x] FUNCS [x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests += 1

        function = Function("f(x) = (x^2,,,,,x^3,,,,,x)")
        if str(function) == "NAME: f VARS: [x] FUNCS [x**2,x**3,x]":
                success+=1
        else:
                FAILED.append(function)
        num_tests+=1

        ##==================== End of things that should be interpreted tests =============================
        print("{}/{} tests passed for Function interpreter as a whole".format(success,num_tests))
        end_time = os.times()[0]
        if FAILED:
                print("The following functions failed the tests:")
                for i in FAILED:
                        print("\t" + str(i))
        print("Testing Function interpreter as a whole took {} seconds.".format(end_time-start_time))

        ## ====================== generate_interpreted tests ==============================================


        ## ======================= end of generate_interpreted tests =====================================