<?php
$home_path="./index.php?logged_in=1";
if(preg_match('/.*\/thank\.php/', $_SERVER['REQUEST_URI']))
{
    $home_path="./login.php";
}
?>
<!doctype html>
<html>
<head>
  <title>Guido</title>
  <meta http-equiv="Content-Type"
        content="application/xhtml+xml; charset=utf-8" />
  <link rel="stylesheet" type="text/css" href="style.css" media="screen" />
</head>
<body>
<a  id="logo" href=<?php print "$home_path";?> ><img border=0 src="./inc/logo.png"></a>
<div id="navmenu" class="pathclass" align="right">
<?php
    $username = $_REQUEST['username'] ;
    $title = "Grade an assignment (Fall 2010): <tt>";
    if(isset($username)){
        $title .= $username;
    }
    $title .= "</tt>";
    if(!preg_match('/.*\/login\.php/', $_SERVER['REQUEST_URI'])
    && !preg_match('/.*\/thank\.php/', $_SERVER['REQUEST_URI']))
    {
        print '
<a href="index.php?logged_in=1" target="_parent">Home</a>&nbsp&nbsp&nbsp&nbsp
<a href="thank.php" target="_parent">Sign Out</a></p>';
    }else{
        print '&nbsp;';
    }
?>
</div>
