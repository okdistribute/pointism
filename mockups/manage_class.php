<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>Admin a class (Fall 2010): <tt>menzel</tt></h1>
</div>
<div id="path">
Admin: <b>Manage Class</b>
</div>
<div id="content">
<table border=0>
<tr>
<td>Manage Students:</td><td width="200" align="right"><button
type="button" onclick="window.location='./student_details.php'">Who is in the class?
</button></td></tr>
<tr>
<td>Manage TAs:</td><td width="200" align="right"><button
type="button" onclick="window.location='./ta_details.php'">Who is TA?
</button></td></tr>
<tr>
</table>
</div>
<?php
    include("inc/footer.inc");
?>
