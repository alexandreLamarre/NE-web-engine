# NE Computational Engine

## Foreword


A computational engine is hard to define, but easy to recognize. 
In general a computation engine takes some aggregation of data and returns a meaningful result. 
This implementation of a computational engine 
takes symbolic mathematical input from the user, computes its properties and returns them in a way humans can understand. 
 
**The overarching goal of this computational engine** is to provide users with a **hybrid computational engine** that combines the best of **WolframAlpha and Symbolab**. On one hand, it should provide a **flexible interpreter** and an **abundance of information** while on the other hand, it should remain **easy to use and self contained**, even for the most complicated features. As an additional improvement to these two outstanding engines, we also seek to **generalize problems** that are currently only solvable by these engines in three dimensions to any dimension as well as providing **information about the fundamental structures behind the behaviour of mathematical objects**.
  

## Table of Contents
- [Features](#Features)
- [Quick guide](#Quick-guide)
- [Documentation](#Documentation)
- [Code architecture](#Code-architecture)
- [Implementation details](#Implementation-details)
- [Known issues](#Known-issues)
- [External Libraries](#External-Libraries)
- [References](#References)


## Features: 
- Command interpreter for commands of the form`\command_name{arguments}`
- Function Interpreter:
  - Interprets **custom** mathematical functions from input into python computable functions
  - Makes use of the math standard library for python
  
- Plotting functions for custom mathematical functions for:
  - Functions from R to R <sup></sup> using a traditional graph
  - Functions from R to R<sup>2</sup> using meshgrid technology
  - Functions from R<sup>2</sup> to R using meshgrid technology
  - Functions from R<sup>2</sup> to R<sup>2</sup> using contour maps
  
- Symbolic computation of zeroes of a function in terms of every variable

- Symbolic computation of partial derivatives of a function in terms of every variable

- Symbolic computation of integrals of a function in terms of every variable

  
## Quick guide
 
### Functions

Functions have the syntax `functionname(variables) = (functions)` where ` functionname` is a sequence of letters and digits containing no spaces, `variables` is a list of variables that are a sequence of letters separated by a commas and where `functions` are a list of functions separated by commas that are the [operations](#operations) on those defined variables. See some examples [here](#examples). Multiple functions can be defined in the same line: `function1(x) = (x) function2(x) = (x^2) ...` will be interpreted as multiple functions. Functions support a variety of [Standard functions](#common). **Before reporting a bug**, check out our [**known issues**](#Known-issues).

### Commands on Functions


Commands have the syntax `commandname{data}` where `commandname` is a sequence of letters containing no spaces.

- Plot: syntax: `plot{functions}`. Supports multiple functions.
- Zeroes: syntax: `zeroes{functions}.` Supports multiple functions. 
- Partial derivative: `partialderivative{functions}`. Supports multiple functions.
- Partial integral: `partialintegral{functions}`. Supports multiplew functions

## Documentation:

### Computational Engine: Functions

- To first use the engine, we must define a function. For our purposes, a function requires a **name**, a **set of variables**, and a **set of output functions**.
  
- For the website to recognize your input, we must define a function in a way that our interpreter will understand. We do so by providing a **function name** comprised of **only letters and digits**, followed by a **set of variables in between parentheses** `(a,b,c,d,...)`, where each variable name is comprised of **only letters**, **has no spaces** in it and each name is **separated by a comma**. Then the input must be followed by an **equals sign** `=` and a **set of parentheses** `(______)` which contain a **set of functions**, each **separated by a comma**. **Parentheses** in a function **must always match** or the interpreter will not recognize your input and will tell you that something is wrong!

- We give some **examples** of recognized functions to help illustrate:
    - `f(x) = (x)`
    - `f    (     x     )   =   ( x    )`, spaces do not effect the input as long as they do not occur in variable names
    - `functionname1(a,b,c) = (a,b,c) `, is also valid
    - `f2(cat,dog) = (cat,dog)`, variables can be of any length as long as they are not separated by spaces
    - `f3(cat   , dog) = (cat,dog)` is **valid** but `f(c at, dog) = (c at,dog)` is **not valid**
 
 - Now that we can define some functions, let's take a look at what **operations between variables** are supported in the functions we want to define:
    - `+` is standard addition
    - `-` is standard subtraction
    - `*` is standard multiplication
    - `**` and `^` are standard exponentiation.
    
- We give some **examples** of the operators in our functions.
    - `f(x) = (x*x)`
    - `f(x) = (x*(x+1))`
    - `f(x,y) = (x**2 + y**2, x - y)`
    
- By default if **no operation** is given, **the interpreter will guess** how to interpret it:
    - `f(x) = (xx)` is equivalent to `f(x) = (x*x)` and `f(x) = (x^2)` and `f(x) = (x**2)`
    - `f(x,y) = (xy)` is equivalent to `f(x,y) = (x*y)`
    - `f(cat,a) = (catacataaa)` is equivalent to `f(cat,a) = (cat*a*cat*a^3)`
    - `f(x,y) = ((x)x(y+1))` is equivalent to `f(x,y) = (x^2*(y+1))`
    - etc...
    
- The interpreter also recognizes the following **common mathematical functions** to the best of its ability:
    - `abs`,`log`,`cos`, `sin`, `tan`,`ceil`, `ceiling`,`factorial`,`floor`, `isqrt`, `trunc`, `exp`, `log2`, `log10`, `sqrt`, `acos`,`asin`, `atan`,`degrees`, `radians`, `acosh`, `asinh`, `atanh`, `cosh`, `sinh`, `tanh`, `erf`, `erfc`, `gamma`, `lgamma`

- **For these common functions you must provide parentheses** to what they act on, or the interpreter will tell you something is wrong:
    - `f(x) = (log(x))` is **valid** while `f(x) = (log x )` is **not valid**
    
- We give some **examples** of using common mathematical functions in our input:
  - `f(x,y) = (cos(x+y))`, we can include as many variables in their scope as we want
  - `f(cat,dog) = (cat+ log(cat sin( dog cos(dog cat))))`, we can nest as many 'standard' functions as we want, but performance will suffer if too many are nested.
  - You can find **additional explanation** about what these functions do at this [**link**](https://docs.python.org/3/library/math.html).

- The interpreter also comes with the **common math constants** `pi`, `e`, and `tau`, but be careful if you define one of these as a variable, you won't be able to use it as a constant!
    - `f(e) = (e)` is equivalent to `f(x) = (x)` not `f(x) = (e)` where e is the constant `2.76...`
    - `f(pied,pie,pi) = (piedpiepipiedpipie)` is equivalent to `f(pied,pie,pi) = (pied*pie*pi*pied*pi*pie)` and `f(x,y,z) = (x*y*z*x*z*y)` but not `f(x,y,z) = (x*y*pi*x*pi*y)` where `pi` is the constant `3.14159265358979...`

- If your **input is not recognized**, the compiler will tell you so and attempt to give you the reason why the input was rejected. 
    - `Mismatched parentheses` mean 

## Implementation details

- Function variables overshadow math standard 
library variables and functions. 
    - For example,
`f(e) = (e^2)` is equivalent to `g(x) = (x^2)`


<!---
- Iterated Function Systems:
  - [x] Plot 
  - [ ] Associated Markov Chain
  - [ ] Dimension computations
 
- Markov Chains
  - [ ] Visualizer 
  - [ ] Encoding
  - [ ] Properties Evaluator
 
 - Group Theory
   - [ ] Group operations
 
 - Galois Theory
   - [ ] Exact roots of polynomials
   - [ ] Properties Evaluator
--->

## Known issues
- Plots from R2 to R2 appear stringy and not 3-dimensional, unfortunately we are looking at ways to adapt our contour maps to mesh-grid technology. 

- Complex casting happens in exponential and logarithmic functions in contour maps from R<sup>2</sup> to R<sup>2</sup> when they involve multiplevariables when complex casting should not occur. Issue likely has to do with the implementation of the math standard library. 

- Sometimes the latex interpreter on the server side cannot interpret complex latex expressions, and will return an error like the following:
  - `\begin{cases} x \operatorname{acos}{\left(x \operatorname{asin}{\left(y \right)} \right)} - \frac{\sqrt{- x^{2} \operatorname{asin}^{2}{\left(y \right)} + 1}}{\operatorname{asin}{\left(y \right)}} & \text{for}\: y \neq 0 \\\frac{\pi x}{2} & \text{otherwise} \end{cases} ^ Unknown symbol: \begin, found '\' (at char 0), (line:1, col:1)`
  - This will be fixed once the MathJaxHub Queue is fixed, as the server will no longer need to process latex internally and reformat it as an image using third party libraries, but will be rendered directly in the browser from its latex string. 

- `e`,`tau`, `erf`, `erfc`, `log2`, `log10`, `lgamma` and potentially other common functions from the math standard library are not necessarily compatible with symbolic computation. An error of the type `name not defined` or `Symbol not recognized` will be output in this case. This issue will be fixed in a later version. 

- 'Zeroes' information tab will sometimes insist that a root must be complex when it is clearly not necessarily a complex root.

## External Libraries
- [NumPy](https://numpy.org)
- [Matplotlib](https://matplotlib.org/)
- [regex](https://pypi.org/project/regex/)
- [SymPy](https://www.sympy.org/en/index.html)

## References
  

  - Tucker, Alan. "Applied Combinatorics" 6th edition 2012
  - Munkres, James R. "Topology" 2nd edition. 2018.
  - Fisher, Stephen D. "Complex Variables" 1990.
  - Folland, Gerald B.  "Advanced Calculus" 2002.

## Running development server commands


  yarn start
    Starts the development server.

  yarn build
    Bundles the app into static files for production.

  yarn test
    Starts the test runner.

  yarn eject
    Removes this tool and copies build dependencies, configuration files
    and scripts into the app directory. If you do this, you can’t go back!

