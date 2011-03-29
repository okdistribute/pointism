;; ---- hereis.ss

(define myprintf
  (lambda (fs . xs)
    (myformat-main 'myprintf (current-output-port) fs xs)))

(define myfprintf
  (lambda (op fs . xs)
    (myformat-main 'myfprintf op fs xs)))

(define myformat
  (lambda (fs . xs)
    (let ([op (open-output-string)])
      (myformat-main 'myformat op fs xs)
      (get-output-string op))))

(define myformat-main
  (lambda (name op fs xs)
    (let ([ip (open-input-string fs)])
      ;; ---- begin parser states
      (define start
        (lambda (xs)
          (let ([c (read-char ip)])
            (cond
              [(eof-object? c)
               (unless (null? xs)
                 (error name "Too many arguments for format string ~s" fs))]
              [(char=? c #\~)
               (sign xs)]
              [else
                (write-char c op)
                (start xs)]))))
      (define sign
        (lambda (xs)
          (let ([c (peek-char ip)])
            (case c
              [(#\- #\+)
               (read-char ip)
               (signed-integer-maybe xs c)]
              [else (integer-maybe xs)]))))
      (define signed-integer-maybe
        (lambda (xs sign)
          (let ([c (peek-char ip)])
            (cond
              [(char<=? #\0 c #\9)
               (read-char ip)
               (integer xs sign (char->digit c))]
              [else
                (control-error sign c)]))))
      (define integer-maybe
        (lambda (xs)
          (let ([c (peek-char ip)])
            (cond
              [(char<=? #\0 c #\9)
               (read-char ip)
               (integer xs #\+ (char->digit c))]
              [else
                (fchar-nofill xs)]))))
      (define integer
        (lambda (xs sign acc)
          (let ([c (peek-char ip)])
            (cond
              [(char<=? #\0 c #\9)
               (read-char ip)
               (integer xs sign (+ (* acc 10) (char->digit c)))]
              [else
                (fchar-fill xs (if (char=? sign #\-)
                                   (- acc)
                                   acc))]))))
      (define fchar-nofill
        (lambda (xs)
          (let ([c (read-char ip)])
            (if (eof-object? c)
                (control-error "")
                (case c
                  [(#\s)
                   (when (null? xs) (length-error))
                   (write (car xs) op)
                   (start (cdr xs))]
                  [(#\a)
                   (when (null? xs) (length-error))
                   (display (car xs) op)
                   (start (cdr xs))]
                  [(#\c)
                   (when (null? xs) (length-error))
                   (unless (char? (car xs))
                     (error name "~s is not a character for format string ~s"
                       (car xs) fs))
                   (write-char (car xs) op)
                   (start (cdr xs))]
                  [(#\% #\n)
                   (write-char #\newline op)
                   (start xs)]
                  [(#\~)
                   (write-char c op)
                   (start xs)]
                  [else
                    (control-error c)])))))
      (define fchar-fill
        (lambda (xs fill)
          (let ([c (read-char ip)])
            (if (eof-object? c)
                (control-error fill "")
                (case c
                  [(#\s)
                   (when (null? xs) (length-error))
                   (do-fill fill write (car xs) op)
                   (start (cdr xs))]
                  [(#\a)
                   (when (null? xs) (length-error))
                   (do-fill fill display (car xs) op)
                   (start (cdr xs))]
                  [else
                    (control-error fill c)])))))
         ;; ---- end parser states

      (define char->digit
        (lambda (c)
          (- (char->integer c) 48)))
      (define pad
        (lambda (n op)
          (unless (<= n 0)
            (write-char #\space op)
            (pad (- n 1) op))))
      (define do-fill
        (lambda (fill func x op)
          (let ([temp (open-output-string)]
                [fillsize (abs fill)])
            (func x temp)
            (let* ([str (get-output-string temp)]
                   [len (string-length str)])
              (cond
                [(negative? fill)
                 (pad (- fillsize len) op)
                 (display str op)]
                [else
                  (display str op)
                  (pad (- fillsize len) op)])))))
      (define control-error
        (case-lambda
          [(thing) (error name "Invalid control ~~~a in ~s" thing fs)]
          [(thing1 thing2)
           (error name "Invalid control ~~~a~a in ~s" thing1 thing2 fs)]))
      (define length-error
        (lambda ()
          (error name "Too few arguments for format string ~s" fs)))
      (start xs))))

;;(define-syntax hereis
;;  (let ()
;;    (define-syntax try/error
;;      (syntax-rules ()
;;        [(_ exp handler)
;;         (call/cc
;;           (lambda (k)
;;             (parameterize
;;                 ([error-handler
;;                    (let ([old-error-handler (error-handler)])
;;                      (lambda args
;;                        (parameterize ([error-handler old-error-handler])
;;                          (call-with-values
;;                              (lambda () (apply handler args))
;;                            k))))])
;;               (call-with-values
;;                   (lambda () exp)
;;                 k))))]))
;;    (define parse
;;      (lambda (str)
;;        (let ([ip (open-input-string str)]
;;              [op (open-output-string)])
;;          (define start
;;            (lambda (xs)
;;              (let ([c (read-char ip)])
;;                (cond
;;                  [(eof-object? c)
;;                   (values (get-output-string op) (reverse xs))]
;;                  [(char=? c #\~)
;;                   (write-char c op)
;;                   (sign xs)]
;;                  [else
;;                    (write-char c op)
;;                    (start xs)]))))
;;          (define sign
;;            (lambda (xs)
;;              (let ([c (peek-char ip)])
;;                (case c
;;                  [(#\- #\+)
;;                   (read-char ip)
;;                   (write-char c op)
;;                   (signed-integer-maybe xs c)]
;;                  [(#\~)
;;                   (read-char ip)
;;                   (write-char c op)
;;                   (start xs)]
;;                  [else (integer-maybe xs)]))))
;;          (define signed-integer-maybe
;;            (lambda (xs sign)
;;              (let ([c (peek-char ip)])
;;                (cond
;;                  [(char<=? #\0 c #\9)
;;                   (read-char ip)
;;                   (write-char c op)
;;                   (integer xs)]
;;                  [else
;;                    (error 'hereis "Bad format character ~~~c" sign)]))))
;;          (define integer-maybe
;;            (lambda (xs)
;;              (let ([c (peek-char ip)])
;;                (cond
;;                  [(char<=? #\0 c #\9)
;;                   (read-char ip)
;;                   (write-char c op)
;;                   (integer xs)]
;;                  [else
;;                    (lbrack xs)]))))
;;          (define integer
;;            (lambda (xs)
;;              (let ([c (peek-char ip)])
;;                (cond
;;                  [(char<=? #\0 c #\9)
;;                   (read-char ip)
;;                   (write-char c op)
;;                   (integer xs)]
;;                  [else
;;                    (lbrack xs)]))))
;;          (define lbrack
;;            (lambda (xs)
;;              (let ([c (peek-char ip)])
;;                (cond
;;                  [(char=? c #\{)
;;                   (read-char ip)
;;                   (let ([exp (try/error (read ip)
;;                                (lambda args
;;                                  (error 'hereis "Bad read in ~s" str)))])
;;                     (write-char #\a op)
;;                     (rbrack (cons exp xs)))]
;;                  [else
;;                    (doread xs)]))))
;;          (define rbrack
;;            (lambda (xs)
;;              (let ([c (read-char ip)])
;;                (case c
;;                  [(#\}) (start xs)]
;;                  [(#\space #\tab #\newline)
;;                   (rbrack xs)]
;;                  [else
;;                    (error 'hereis "garbage in brackets: ~s" str)]))))
;;          (define doread
;;            (lambda (xs)
;;              (let ([exp (try/error (read ip)
;;                           (lambda args
;;                             (error 'hereis "Bad read in ~s" str)))])
;;                (write-char #\a op)
;;                (start (cons exp xs)))))
;;          (start '()))))
;;    (lambda (x)
;;      (syntax-case x ()
;;        [(_ str)
;;         (string? (syntax-object->datum (syntax str)))
;;         (call-with-values
;;             (lambda () (parse (syntax-object->datum (syntax str))))
;;           (lambda (fs args)
;;             (let ([plate (syntax _)])
;;               (with-syntax ([fs (datum->syntax-object plate fs)]
;;                             [(arg ...)
;;                              (map (lambda (x)
;;                                     (datum->syntax-object plate x))
;;                                args)])
;;                 (syntax
;;                   (myformat fs arg ...))))))]))))
