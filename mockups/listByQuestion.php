<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Admin/TA: <a href="assignment_list.php">Grade an assignment</a> > <a href="assignment3.php">
Assignment 3</a> > <b>List By
Question</b><font color="grey">  > Grade </font>
</div>
<div id="content">
<h2>You have selected "Assignment 3"</h2>
<table border ="1" cellpadding="10">
<tr>
<th>List of Questions</th>
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
