# NE Computational Engine

## Foreword

A computational engine is hard to define, but easy to recognize. 
In general a computation engine takes some aggregation of data and returns a meaningful result. 
This implementation of a computational engine 
takes symbolic mathematical input from the user, computes its properties and returns them in a way humans can understand. 
 
Traditionally, other mathematical computational engines like Wolfram Alpha(now computational intelligence) focus on 
the fixed three dimensions that we've all seen in high school geometry, high school algebra and college calculus. 
These methods represent simple ways to interpret phenomena and are Euclidean in nature.
In this computational engine, we aim to take things further by also interpreting
the properties of mathematical objects that produce things that are non-euclidean in nature. 
  

## Table of Contents
- [Features](#Features)
- [Quick guide](#Quick-guide)
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
  
- Plotting functions from custom mathematical functions for:
  - Functions from R to R <sup></sup> using a traditional graph
  - Functions from R to R<sup>2</sup> using meshgrid technology
  - Functions from R<sup>2</sup> to R using meshgrid technology
  - Functions from R<sup>2</sup> to R<sup>2</sup> using contour maps
  
  
 
## Quick guide:

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
    
- The interpreter also recognizes the following **common mathematical functions**:
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
- Complex casting happens in exponential and logarithmic functions 
in contour maps from R<sup>2</sup> to R<sup>2</sup> when they involve multiple
variables when complex casting should not occur. Issue likely has to do with the 
implementation of the math standard library. 
 

## External Libraries
- [NumPy](https://numpy.org/doc/)
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

