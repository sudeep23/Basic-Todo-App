%# template to create table from array of dictionaries, needs <header> and <rows>
<p>The items are:</p>
<table border="10">
<tr>
%for key in header:
    <th><i>{{key}}</i></th>
%end
</tr>
%for row in rows:
  <tr>
  %for key in header:
    <td><i>{{row[key]}}</i></td>
  %end
  </tr>
%end
</table>