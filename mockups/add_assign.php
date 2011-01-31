<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>Admin an assignment (Fall 2010): <tt>menzel</tt></h1>
</div>
<div id="path">
Admin: <b>Create an assignment</b> <font color="grey"> > Related
Questions > Distribution > Assign Final Grader </font>
</div>
<div id="content">
<b>This is the second assignment in Fall 2010.</b>
<FORM METHOD=post ACTION="related_assign.php">
<BR>How many questions did you create for the assignment 2? 
<INPUT TYPE="text" NAME="list" SIZE="4">
<INPUT TYPE="submit" VALUE="Submit">
</FORM>
</div>
<?php
    include("inc/footer.inc");
?>
