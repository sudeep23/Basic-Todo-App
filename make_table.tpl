%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<h1>Open Todo  App</h1>

<form action="/new" method="get">
    <td><input type="submit" name="new" value="Create New Item"></td>
</form>

<form action="/todo/closed" method="get">
    <td><input type="submit" name="closed" value="List Closed Items"></td>
</form>

<p>The open items are as follows:</p>
<table border="1">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  <form action="/edit/{{row[0]}}" method="get">
    <td><input type="submit" name="edit" value="edit"></td>
  </form>
  <form action="/delete/{{row[0]}}" method="delete">
    <td><input type="submit" name="delete" value="delete"></td>
  </form>
  </tr>
%end
</table>