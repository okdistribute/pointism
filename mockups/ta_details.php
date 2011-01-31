<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>Admin a class (Fall 2010): <tt>menzel</tt></h1>
</div>
<div id="path" class="pathclass">
Admin: <a href="manage_class.php">Manage Class</a> > <b>Current
TAs </b> 
</div>
<div id="content">
<table border="1">
<tr><th>University ID</th><th>Name</th><th>Term</th><th> &nbsp;</th></tr>
<tr><td align="right">1000</td><td>Brooks, Jason</td><td>Fall 2010</td><td><a href=""><font color="red">Remove</font></a></td></tr>
<tr><td align="right">2100</td><td>Hanks, John</td><td>Fall 2010</td><td><a href=""><font color="red">Remove</font></a></td></tr>
<tr><td align="right">0004</td><td>Smith, Myra</td><td>Fall 2010</td><td><a href=""><font color="red">Remove</font></a></td></tr></table>
<br>
<br>
<br>
Add more TAs? <button type="button">ADD</button>
</div>
<?php
    include("inc/footer.inc");
?>
