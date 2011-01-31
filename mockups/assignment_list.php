<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Admin/TA: <b>Grade an assignment</b> 
</div>
<div id="content">
<h2>ASSIGNMENT LIST</h2>
<table border="1" cellpadding="10">
<tr>
<th>Details</th>
<th>Status</th>
</tr>
<tr>
<td><a href = "assignment3.php?username=<?=$username?>">ASSIGNMENT 1</a></td>
<td><font color="Blue">Graded</font></td>
</tr>
<tr>
<td><a href = "assignment3.php?username=<?=$username?>">ASSIGNMENT 2</a></td>
<td><font color="Blue">Graded</font></td>
</tr>
<tr>
<td><a href = "assignment3.php?username=<?=$username?>">ASSIGNMENT 3</a></td>
<td><font color="Red">Not Graded (500/700)</font></td>
</tr>
</table>
<br><br><br><br><br><br>
<hr />

Choose the assignment you need to view.....
<br><br>
Will you publish the Assignment 3 to the students? <button type="button">YES</button> <button type="button">NO</button>
</div>
<?php
    include("inc/footer.inc");
?>
