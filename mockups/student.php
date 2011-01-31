<?php
    include("inc/header.inc");
?>

<div id="header">
<h1>welcome to guido, <tt>jstudent</tt></h1>
</div>
<div id="path">
Student: View your assignments
</div>
<div id="content">

  <!-- left -->
  <div class="assignmentlist">
    <h2>View your graded assignments</h2>

    <ul>
      <li><a href="feedback.php">a1: Write Scheme</a></li>
      <li><a href="feedback.php">a2: Write more Scheme</a></li>
      <li><a href="feedback.php">a3: Write more Scheme with recursion</a></li>
      <li><a href="feedback.php">a4: Stop writing Scheme</a></li>
    </ul>
  </div>

  <!-- right -->
  <div class="codesearchbox">
  <FORM action="searchresults.php">
    <h2>Search your graded assignments</h2>
    <input class="searchinput" type="textbox"/>
    <input type="submit" value="search">
  </FORM>
    <br/>
  </div>

<br clear="all"/>
</div>
<?php
    include("inc/footer.inc");
?>
