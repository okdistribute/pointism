#!/usr/bin/env python3

"""
Module where we keep fake data for now. Until we pull these things from the
database.
"""

import model

### Fake data for the grading screen.
autograder = "(autograder output goes here)"
student = "jstudent"
assignment = "a5"

studentsolution = """\
(define fac
  (lambda (x)
    (if (< x 2) 1
      (* x (fac (- x 1))))))

(define plusthree
  (lambda (x)
    (+ x 3)))
"""

existingcomment = "Clever approach."

prevcommenttext = \
[
"that will never work.",
"""Here are some reasons why it will never work:
- it's a bad idea
- problematic and ill-conceived.""" 
]

prevcomments = list( map( lambda pair: model.Comment(pair[0],pair[1]),
                          zip(range(len(prevcommenttext)),
                              prevcommenttext)) )
