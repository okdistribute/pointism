<?php
    include("inc/header.inc");
    $logged_in = $_REQUEST['logged_in'] ;
    $URI = preg_replace('/(.*mockups)\/(.*)/','$1/login.php',$_SERVER['REQUEST_URI']);
    $URL="http://" . $_SERVER['SERVER_NAME'] . $URI;
    if(!isset($logged_in)){
        header("location:$URL");
    }
?>
<div id="header">
<h1>Mockup front pages</h1>
</div>
<div id="path">
Front page
</div>
<div id="content">
<p><h2>User Interfaces for C211 Class</h2></center>

<p><a href="instructor.php" class="frontbutton">for the instructor</a></p>
<p><a href="ta.php" class="frontbutton">for the TA</a></p>
<p><a href="student.php" class="frontbutton">for the student</a></p>
</div>
<?php
    include("inc/footer.inc");
?>
