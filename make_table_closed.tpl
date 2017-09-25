%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<h1>Done Items</h1>
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