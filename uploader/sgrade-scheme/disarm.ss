;;; Copyright (c) 2008 R. Kent Dybvig
;;; 
;;; Permission is hereby granted, free of charge, to any person obtaining a
;;; copy of this software and associated documentation files (the "Software"),
;;; to deal in the Software without restriction, including without limitation
;;; the rights to use, copy, modify, merge, publish, distribute, sublicense,
;;; and/or sell copies of the Software, and to permit persons to whom the
;;; Software is furnished to do so, subject to the following conditions:
;;;
;;; The above copyright notice and this permission notice shall be included in
;;; all copies or substantial portions of the Software.
;;;
;;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
;;; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
;;; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
;;; THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
;;; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
;;; FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
;;; DEALINGS IN THE SOFTWARE.

;;; Todo:
;;;   are there other parameters we should disable/restrict?

;;; current model:
;;;   language provided is a safe subset
;;;   names of "disabled" procedures are simply made unbound
;;;   "restricted" procedures don't support nonsafe features
;;;      for example, optimize-level is defined only for no arguments
;;;   no explicit "disabled" messages are given

;;; alternative model:
;;;   disabled procedures complain when invoked
;;;   disabled syntactic forms complain at expand time
;;;   module names are unbound or treated as syntactic forms (not perfect)
;;;   restricted procedures complain on attempt to use restricted features

;;; things we were disarming but aren't now:
;;;   close-input-port
;;;   close-output-port
;;;   eps-expand
;;;   trace-output-port

(define (disarm)
  (let* ([safe-from-scheme
          `(< <= = > >= - / * + -1+ 1- 1+ abs acos acosh add1 alias and
            andmap angle append append! application-expander apply
            apropos apropos-list
            ash asin asinh assoc assq assv
            atan atanh atom? begin bignum? block-read
            block-write boolean? bound-identifier=? box
            box? bwp-object? bytes-allocated caaaar caaadr caaar caadar
            caaddr caadr caar cadaar cadadr cadar caddar cadddr caddr
            cadr call/1cc call/cc call-with-current-continuation
            call-with-values car case case-lambda case-sensitive
            cdaaar cdaadr cdaar cdadar cdaddr cdadr cdar cddaar
            cddadr cddar cdddar cddddr cdddr cddr cdr ceiling cfl=
            cfl- cfl/ cfl* cfl+ cfl-conjugate cfl-imag-part
            cfl-magnitude-squared cflonum? cfl-real-part
            char<=? char<? char=? char>=? char>? char-
            char? char-alphabetic? char-ci<=? char-ci<?
            char-ci=? char-ci>=? char-ci>? char-downcase
            char->integer char-lower-case? char-name
            char-numeric? char-ready? char-upcase
            char-upper-case? char-whitespace? clear-input-port
            clear-output-port close-input-port close-output-port
            close-port collect collect-generation-radix
            collect-maximum-generation collect-notify
            collect-request-handler collect-trip-bytes compile-compressed
            compile-interpret-simple compile-profile complex? cond
            conjugate cons constant-expander cos cosh cp0-effort-limit
            cp0-inner-unroll-limit cp0-outer-unroll-limit cp0-polyvariant
            cp0-score-limit cpu-time critical-section
            current-input-port current-output-port date-and-time
            datum->syntax-object decode-float define define-record
            define-structure define-syntax define-syntax-expander
            define-top-level-value delay denominator disable-interrupts
;;sm            display 
            display-statistics do dynamic-wind
            enable-interrupts 
;;sm eof-object? 
            eps-expand eps-expand-once
            eq? equal? eqv? error eval-syntax-expanders-when eval-when
            even? exact? exact->inexact exp expt expt-mod extend-syntax
            extend-syntax/code fasl-write file-length file-position
            fixnum? fixnum->flonum fl< fl<= fl= fl> fl>= fl- fl/ fl*
            fl+ flabs fllp fl-make-rectangular flonum? flonum->fixnum
            floor fluid-let fluid-let-syntax flush-output-port
            force for-each format fprintf free-identifier=? fx<
            fx<= fx= fx> fx>= fx- fx/ fx* fx+ fx1- fx1+ fxabs
            fxeven? fxlogand fxlognot fxlogor fxlogxor fxmax fxmin
            fxmodulo fxnegative? fxnonnegative? fxnonpositive?
            fxodd? fxpositive? fxquotient fxremainder fxsll fxsra
            fxsrl fxzero? gcd generate-inspector-information
            generate-interrupt-trap generate-temporaries gensym
            gensym? gensym-count gensym-prefix gensym->unique-string
            getenv get-hash-table get-output-string getprop
            hash-table? hash-table-for-each hash-table-map heap-reserve-ratio
            identifier? identifier-syntax if imag-part import import-only
            inexact? inexact->exact input-port? install-expander
            integer? integer->char integer-length isqrt lambda last-pair
            lcm length let let* let-values letrec letrec* letrec-syntax
            let-syntax list
            list? list* list-copy list-ref list->string list-tail
            list->vector literal-identifier=? lock-object log logand
            lognot logor logxor
            machine-type magnitude magnitude-squared make-guardian
            make-hash-table
            make-input/output-port make-input-port make-list
            make-output-port make-parameter make-polar make-record-type
            make-rectangular make-sstats make-string make-vector map
            mark-port-closed! max member memq memv merge merge! meta min
            module modulo most-negative-fixnum most-positive-fixnum
            negative? newline nonnegative? nonpositive? not
            null? null-environment number? number->string numerator
            oblist odd? open-input-string open-output-string
            or ormap output-port? pair? parameterize
            peek-char port? port-closed? port-handler port-input-buffer
            port-input-index port-input-size port-name port-output-buffer
            port-output-index port-output-size positive? pretty-file
            pretty-initial-indent pretty-line-length pretty-maximum-lines
            pretty-one-line-limit pretty-print pretty-standard-indent
            print-brackets printf print-gensym print-graph print-length
            print-level print-radix print-record print-vector-length
            procedure? profile-clear property-list put-hash-table! putprop quasiquote
            quote quotient random random-seed rational? rationalize
            ratnum? 
;;sm read read-char 
            read-token real? real-part
            real-time rec record? record-case record-constructor
            record-field-accessible? record-field-accessor
            record-field-mutable? record-field-mutator
            record-predicate record-reader
            record-type-descriptor? record-type-field-decls
            record-type-field-names record-type-interfaces record-type-name
            record-type-parent record-type-symbol record-writer
            remainder remove remove! remove-foreign-entry remove-hash-table!
            remprop remq remq! remv remv! reverse reverse! round
            set! set-box! set-car! set-cdr! set-port-input-index!
            set-port-input-size! set-port-output-index!
            set-port-output-size! set-sstats-bytes! set-sstats-cpu!
            set-sstats-gc-bytes! set-sstats-gc-count! set-sstats-gc-cpu!
            set-sstats-gc-real! set-sstats-real!  set-top-level-value!
            sin sinh sort sort! source-directories sqrt
            sstats? sstats-bytes sstats-cpu sstats-difference
            sstats-gc-bytes sstats-gc-count sstats-gc-cpu
            sstats-gc-real sstats-print sstats-real statistics
            string string<=? string<? string=? string>=?
            string>? string? string-append string-ci<=? string-ci<?
            string-ci=? string-ci>=? string-ci>? string-copy
            string-fill! string-length string->list
            string->number string-ref string-set! string->symbol
            sub1 subst subst! substq substq! substring
            substring-fill! substv substv! suppress-greeting
            symbol? symbol->string syntax syntax-case syntax-error
            syntax-match? syntax-object->datum syntax-rules tan
            tanh time top-level-bound? top-level-value
            trace trace-case-lambda trace-define trace-define-syntax
            trace-lambda trace-let trace-output-port trace-print
            truncate type-descriptor unbox unless unlock-object
            unquote unquote-splicing unread-char untrace
            values variable-expander vector vector? vector-copy
            vector-fill! vector-length vector->list vector-ref
            vector-set! void waiter-prompt-and-read waiter-prompt-string
            waiter-write warning weak-cons weak-pair? when with-syntax

copy-environment
environment?
trace-do
display-string

environment-symbols ; ?
with-input-from-string
with-output-to-string

;;sm            write write-char 
            zero?
          ; new in V7.1
           syntax->list logior profile-dump list-head unsyntax-splicing
           logbit? logbit1 logbit0 syntax->vector fxlogior
           with-implicit pretty-format expand/optimize quasisyntax
           fxlogbit?  fxlogbit1 fxlogbit0 datum logtest fxlogtest unsyntax
           flround
          ,@(if (top-level-bound? 'vector-set-fixnum!)
                '(vector-set-fixnum!)
                '())

          ; new in V7.3
            fxvector-set! make-fxvector fxvector-length list->fxvector
            fxvector-copy fxvector? fxvector-fill! fxvector->list
            fxvector fxvector-ref

          ; new in V7.4
	   default-prompt-and-read exact hashtable-ref date-day
	   eq-hashtable-set! hashtable-cell date-hour fold-right
	   path-parent hashtable-clear! hashtable-delete!  path-root
	   time? time-second time-nanosecond hashtable-mutable? 
	   hashtable-entries make-time for-all remp meta-cond
	   eq-hashtable-delete! inexact date-week-day fold-left cons*
	   date-year-day eq-hashtable? boolean=?  memp iota
	   make-weak-eq-hashtable path-last hashtable-contains? 
	   current-time eof-object date-minute eq-hashtable-cell
	   eq-hashtable-ref find assp eq-hashtable-weak? 
	   date-zone-offset hashtable-size vector-map date-month
	   set-port-bol! date?  let*-values make-eq-hashtable enumerate
	   set-time-second! date-nanosecond set-time-nanosecond! 
	   syntax->datum vector-sort datum->syntax list-sort date-second
	   time>? make-date time=?  time<?  hashtable-set! 
	   directory-separator profile-dump-list hashtable? 
	   directory-separator? hashtable-update!  date-year partition
	   hashtable-keys filter time>=? eq-hashtable-contains?  time<=? 
	   vector-for-each symbol=? fresh-line profile-palette exists
	   current-date set-time-type! eq-hashtable-update! 
	   path-extension vector-sort! hashtable-copy time-type

          )]
         [disable
          '(abort abort-handler break
            break-handler call-with-input-file call-with-output-file
            cd command-line-arguments compile compile-file compile-port

   compile-script
   chmod
   mkdir
   scheme-environment

            console-input-port console-output-port
            current-directory current-eval current-expand
            debug delete-file engine-block engine-return
            error-handler exit exit-handler fasl-file
            file-exists? foreign-callable
            foreign-callable-entry-point foreign-entry?
            foreign-procedure ieee
            ieee-environment include inspect inspect/object
            interaction-environment internal-defines-as-letrec*
            keyboard-interrupt-handler
            load-shared-object make-boot-header make-engine new-cafe
            open-input-output-file 
;;sm open-input-file open-output-file
            |#primitive|
            process putenv r5rs r5rs-syntax record-type-descriptor register-signal-handler
            reset reset-handler revisit run-cp0
            scheme-report-environment scheme-script scheme-start set-timer
            subset-mode system |#system| timer-interrupt-handler
            transcript-cafe transcript-off transcript-on
            truncate-file
            visit warning-handler with-input-from-file
            with-output-to-file with-source-path

          ; new in V7.1
            command-line

          ; new in V7.4
	    directory-list delete-directory profile-dump-html
	    expression-editor file-symbolic-link? file-regular? 
	    file-directory? rename-file

          )]
         [variable-redefinitions
          `((define-read-only optimize-level
              (lambda ()
                (import scheme)
                (optimize-level)))
            (define-read-only eval
              (lambda (e) (import scheme) (eval e)))
            (define-read-only expand
              (lambda (e) (import scheme) (expand e)))
            (define-read-only interpret
              (lambda (e) (import scheme) (interpret e)))
            (define-read-only load
              (lambda args 
                ;(warning 'load "ignoring load")
                (void)))
            (define-read-only sc-expand
              (lambda (e) (import scheme) (sc-expand e))))]
         [export-list
          `(,@safe-from-scheme
            ,@(map cadr variable-redefinitions))])
   ; make sure we haven't missed (or invented) any scheme exports
    (let ([all-scheme-exports
           (let ()
            ; from v7.1 syntax.ss
             (define-record #{interface |<-hmqpg*3t-ak\\%|} ((immutable marks) (immutable exports) (immutable token)))
             (syntax-object->datum
               (vector->list
                 (interface-exports
                   (cdr (#%|#sgetprop| 'scheme '*cte* #f))))))]
          [all-vars-handled `(,@export-list ,@disable scheme)])
      (define difference
        (lambda (ls1 ls2)
          (if (null? ls1)
              '()
              (if (memq (car ls1) ls2)
                  (difference (cdr ls1) ls2)
                  (cons (car ls1) (difference (cdr ls1) ls2))))))
      (let ([extra-scheme-exports (difference all-scheme-exports all-vars-handled)])
        (unless (null? extra-scheme-exports)
          (void)  ;; sm
          ;(pretty-print extra-scheme-exports)
          ;(warning 'disarm.ss "unhandled scheme exports")
          ))
      (let ([extra-vars-handled (difference all-vars-handled all-scheme-exports)])
        (unless (null? extra-vars-handled)
          (pretty-print extra-vars-handled)
          (warning 'disarm.ss "non-scheme exports handled"))))
    (eval
      `(begin
        ; build a safe version of the scheme module that contains
        ; safe imports from Scheme plus others redefined safely
         (module safe-scheme ,export-list
           (module ,safe-from-scheme (import scheme))
           (define-syntax define-read-only
             (lambda (x)
               (syntax-case x ()
                 [(_ i-outer e-outer)
                  #'(module ((i-outer i*))
                      (define i* (rec i-outer e-outer))
                      (define-syntax i-outer
                        (cons 'macro!
                          (lambda (x)
                            (syntax-case x (set!)
                              [(set! i e)
                               (syntax-error x
                                 "attempt to assign read-only variable in")]
                              [(i x (... ...)) #'(i* x (... ...))]
                              [i (identifier? #'i) #'i*])))))])))
           ,@variable-redefinitions)
        ; copy redefined-safely exports to top level
         ,@(map (lambda (x)
                  `(set-top-level-value! ',x (let () (import safe-scheme) ,x)))
                (map cadr variable-redefinitions))
        ; make things we don't support squawk
        ; define variable first in to catch any code already compiled
         ,@(map (lambda (x)
                  `(',define-top-level-value
                     ',x
                     ',(lambda args 
                         ; silently ignore disabled procedures
                         (void)
                         ; (error x "disabled")
                         )))
                disable)
        ; define syntax second to catch any new code when expanded
         ,@(map (lambda (x)
                  `(define-syntax ,x
                     (lambda (stx)
                       (syntax-error stx "disabled"))))
                disable))))
 ; alias scheme to safe-scheme
  (eval
    '(let-syntax ([define-alias
                   (lambda (x)
                     (lambda (e)
                       (syntax-case x ()
                         [(k id1 id2)
                          (with-syntax ([b (datum->syntax-object #'k (e #'id2))])
                            #'(define-syntax id1 'b))])))])
       (define-alias scheme safe-scheme))))
