<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>User Login</h1>
</div>
<div id="path">
Login:
</div>
<div id="content">
<p>
<form>
<table>
<tr>
<td>User name: </td><td colspan="2"><input type="text" name="login" /></td></tr>
<td>Password: </td><td><input type="password" name="pwd" /></td><td>
<button type="button" onclick = "window.location='index.php?logged_in=1'">Log
In</button></td></tr>
</table>
</div>
<?php
    include("inc/footer.inc");
?>
