<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Final Grader: <b>Students</b> <font color="grey"> > Give a grade </font>
</div>
<div id="content">
<h2>The current assignment is "Assignment 3"</h2>
<table border ="1" cellpadding="10">
<tr>
<th>Student names</th>
</tr>
<tr>
<td><a href = "give_grade.php?username=<?=$username?>">Joey</a></td>
</tr>
<tr>
<td><a href = "give_grade.php?username=<?=$username?>">Bob</a></td>
</tr>
<tr>
<td><a href = "give_grade.php?username=<?=$username?>">Michael</a></td>
</tr>
</table>
</div>
<?php
    include("inc/footer.inc");
?>
