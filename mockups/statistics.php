<?php
    include("inc/header.inc");
?>
<div id="header">
<h1>Assignment Statistics</h1>
</div>
<div id="path">
TA/Admin: Assignment Statistics 
</div>
<div id="content">


<table border=0>
  <tr>
  <td colspan=2>
    <h2>Within assignments</h2>
    <p>See the distribution of grades for each problem.</p>
  </tr>

  <tr>
  <td>
  Assignment:
  </td>
  <td>
    <select>
      <option value="a1">a1</option>
      <option value="a2">a2</option>
      <option value="a3">a3</option>
      <option value="a4">a4</option>
      <option value="a5">a5</option>
    </select>
  </td>
  </tr>

  <tr>
  <td>split by:</td>
  <td>
    <select>
      <option selected value="wholeclass">whole class (don't split)</option>
      <option value="section">section</option>
      <option value="major">major</option>
      <option value="year">year</option>
    </select>
  </td>
  </tr>

  <tr>
  <td>output as:</td>
  <td>
    <select>
      <option selected value="histogram">histograms</option>
      <option value="boxplot">boxplot</option>
    </select>
  </td>
  </tr>

  <tr>
  <td></td><td><button>Calculate!</button></td>
  </tr>

  <tr>
  <td colspan=2>
  <h2>Whole assignments</h2>
  <p>
  See the distribution of grades for each assignment.
  </p>
  </td>
  </tr>

  <tr>
  <td>
  Assignment:
  </td>
  <td>
    <select>
      <option selected value="all">All assignments</option>
      <option value="a1">a1</option>
      <option value="a2">a2</option>
      <option value="a3">a3</option>
      <option value="a4">a4</option>
      <option value="a5">a5</option>
    </select>
  </td>
  </tr>

  <tr>
  <td>split by:</td>
  <td>
    <select>
      <option selected value="wholeclass">whole class (don't split)</option>
      <option value="section">section</option>
      <option value="major">major</option>
      <option value="year">year</option>
    </select>
  </td>
  </tr>

  <tr>
  <td>output as:</td>
  <td>
    <select>
      <option selected value="histogram">histograms</option>
      <option value="boxplot">boxplot</option>
    </select>
  </td>
  </tr>

  <tr>
  <td></td><td><button>Calculate!</button></td>
  </tr>
</table>
</div>
<?php
    include("inc/footer.inc");
?>
