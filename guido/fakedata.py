#!/usr/bin/env python3

"""
Module where we keep fake data for now. Until we pull these things from the
database.
"""

autograder = "(autograder output goes here)"

studentsolution = """\
(define fac
  (lambda (x)
    (if (&lt; x 2) 1
      (* x (fac (- x 1))))))

(define plusthree
  (lambda (x)
    (+ x 3)))
"""

existingcomment = "Clever approach."
