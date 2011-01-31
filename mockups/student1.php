<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Admin/TA: <a href="assignment_list.php">Grade an assignment</a> > <a href="assignment3.php">
Assignment 3</a> > <a href="listByStudent.php">List By
Student</a> > <b>Student 1</b> <font color="grey"> > Grade </font>
</div>
<div id="content">
<h2>You have selected "Student 1" in "Assignment 3"</h2>
<table border ="0" cellpadding="10">
<tr>
<th>Student 1's answers</th>
</tr>
<tr>
<td><a href = "grading.php?username=<?=$username?>">Question 1</a></td>
</tr>
<tr>
<td><a href = "grading.php?username=<?=$username?>">Question 2</a></td>
</tr>
<tr>
<td><a href = "grading.php?username=<?=$username?>">Question 3</a></td>
</tr>
</table>
</div>
<?php
    include("inc/footer.inc");
?>
