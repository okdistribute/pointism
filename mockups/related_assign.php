<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>Admin an assignment (Fall 2010): <tt>menzel</tt></h1>
</div>
<div id="path" class="pathclass">
Admin: <a href="add_assign.php">Create an assignment</a> > <b>Related
Questions</b> <font color="grey"> > Distribution > Assign Final Grader </font>
</div>
<div id="content">
<b>This is the second assignment in Fall 2010.</b>&nbsp; =>
<font color="red">Assignment 2 has 7 questions</font>
<FORM METHOD=post ACTION="">
<BR>How many group of related questions do you have? 
<INPUT TYPE="text" NAME="list" SIZE="4" VALUE="2">
<INPUT TYPE="submit" VALUE="Submit">
</FORM>
<p>
<FORM METHOD=post ACTION="distribution.php">
<input type="checkbox" name="option1" value="1" checked> 1<br>
<input type="checkbox" name="option2" value="2" checked> 2<br>
<input type="checkbox" name="option3" value="3" checked> 3<br>
<input type="checkbox" name="option4" value="4"> 4<br>
<input type="checkbox" name="option5" value="5"> 5<br>
<input type="checkbox" name="option6" value="6"> 6<br>
<input type="checkbox" name="option7" value="7"> 7<br>
<hr width="80%" align="left">
<input type="checkbox" name="option1" value="1"> 1<br>
<input type="checkbox" name="option2" value="2"> 2<br>
<input type="checkbox" name="option3" value="3"> 3<br>
<input type="checkbox" name="option4" value="4"> 4<br>
<input type="checkbox" name="option5" value="5" checked> 5<br>
<input type="checkbox" name="option6" value="6" checked> 6<br>
<input type="checkbox" name="option7" value="7" checked> 7<br>
<br>
<INPUT TYPE="submit" VALUE="Submit">
</FORM>
</div>
<?php
    include("inc/footer.inc");
?>
