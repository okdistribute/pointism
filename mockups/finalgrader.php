<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>Admin an assignment (Fall 2010): <tt>menzel</tt></h1>
</div>
<div id="path" class="pathclass">
Admin: <a href="add_assign.php">Create an assignment</a> > <a
href="related_assign.php">Related Questions</a> > <a href="distribution.php">Distribution</a>
 > <b>Assign Final Grader</b>
</div>
<div id="content">
<b>This is the second assignment in Fall 2010.</b>&nbsp; =>
<font color="red">Assignment 2 has 7 questions</font>
<p>
<FORM METHOD=post ACTION="">
<br><br>
Final Grader: 
<select>
  <option value="">Select TA</option>
  <option value="dikim">DongInn Kim</option>
  <option value="yuangao">Yuan Gao</option>
  <option value="alexr">Alex Rudnick</option>
</select>
<br><br>
<INPUT TYPE="submit" VALUE="Submit">
</FORM>
</div>
<?php
    include("inc/footer.inc");
?>
