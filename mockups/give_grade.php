<?php
    include("inc/header.inc");
?>
<div id="header">
<h1><?php print $title; ?></h1>
</div>
<div id="path" class="pathclass">
Final Grader: <a
href="give_grade2student.php?username=<?=$username?>">Students</a> >
<b>Give a grade to Joey</b>
</div>
<div id="content">
<h2>The current assignment is "Assignment 3"</h2>
<table border ="1" cellpadding="10">
<tr>
<th colspan="2" align="center" >Joey's questions</th>
</tr>
<tr>
<td><a href = "">Question 1</a></td><td>A</td>
</tr>
<tr>
<td><a href = "">Question 2</a></td><td>B</td>
</tr>
<tr>
<td><a href = "">Question 3</a></td><td>A</td>
</tr>
<tr>
<td><a href = "">Question 4</a></td><td>B</td>
</tr>
<tr>
<td><a href = "">Question 5</a></td><td>A</td>
</tr>
<tr>
<td><a href = "">Question 6</a></td><td>A</td>
</tr>
<tr>
<td><a href = "">Question 7</a></td><td>C</td>
</tr>
</table>
<br>
&nbsp;Average grade: B
<br><br>
<FORM Action="">
Final grade: 
    <select>
      <option value=""></option>
      <option value="A">A</option>
      <option value="B">B</option>
      <option value="C">C</option>
      <option value="D">D</option>
      <option value="F">F</option>
    </select>
    <input type="Submit" value="Submit">
</FORM>
<br>
<br><br>
<button type="button"><&lt;Previous student </button> <button type="button">Next student>></button>
</div>
<?php
    include("inc/footer.inc");
?>
