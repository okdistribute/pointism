<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Admin/TA: <a href="assignment_list.php">Grade an assignment</a> &gt; <a href="assignment3.php">
Assignment 3</a> &gt; <a href="listByQuestion.php">List By
Question</a> &gt; <b>Grade</b>
</div>

<div id="content">

  <h2>problem 1</h2>

  <!-- left -->
  <div class="student">
    <div class="code">
    <div class="linenumbers">
    1<br/> 2<br/> 3<br/> 4<br/> 5<br/> 6<br/> 7<br/> 8<br/>
    </div>
(define fac<br/>
&nbsp;&nbsp;(lambda (x)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;(if (&lt; x 2) 1<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(* x (fac (- x 1))))))<br/>
<br/>
(define plusthree<br/>
&nbsp;&nbsp;(lambda (x)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;(+ x 3)))<br/>
    </div>

    <input type="textbox"> <button>Search code</button>
  </div>

  <!-- right -->
  <div class="grading">
    <p>autograder output goes here</p>

    <select>
      <option value="A">A</option>
      <option value="B">B</option>
      <option value="C">C</option>
      <option value="D">D</option>
      <option value="F">F</option>
    </select>
    <button>grade</button>
    <br/>
    <textarea cols=60>comments?</textarea>

    <p style="margin-bottom:0">Previously used comments:</p>
    <select class="prevcomments" size="3">
      <option>
      Clever approach to the problem; well done!
      </option>
      <option>
      Is it possible to do this without using set! ?
      </option>
      <option>
      How would this work if you did it non-recursively?
      </option>
      <option>
      Very close! Did you consider the case of getting an empty list?
      </option>
      <option>
      Did you even read the problem?
      </option>
    </select>
    <p>Comment autosearch: <input type="textbox"></p>
  </div>

  <br clear="all"/>
</div>
<?php
    include("inc/footer.inc");
?>
