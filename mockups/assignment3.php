<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Admin/TA: <a href="assignment_list.php">Grade an assignment</a> >
<b>Assignment 3</b><font color="grey">  > List By Student / List By
Question > Grade </font>
</div>
<div id="content">
<h2>You have selected "Assignment 3"</h2>
<ul>
<li><a href = "listByStudent.php?username=<?=$username?>">List by Student</a></li>
<li><a href = "listByQuestion.php?username=<?=$username?>">List by Question</a></li>
</ul>
</div>
<?php
    include("inc/footer.inc");
?>
