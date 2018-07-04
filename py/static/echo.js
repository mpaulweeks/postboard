// https://stackoverflow.com/a/7220510
// http://jsfiddle.net/KJQ9K/554/
function output(inp) {
  document.getElementById('output').innerHTML = inp;
}
function syntaxHighlight(json) {
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
    var cls = 'number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) {
        cls = 'key';
      } else {
        cls = 'string';
      }
    } else if (/true|false/.test(match)) {
      cls = 'boolean';
    } else if (/null/.test(match)) {
      cls = 'null';
    }
    return '<span class="' + cls + '">' + match + '</span>';
  });
}

document.body.innerHTML = `
  <h1>Form Echo</h1>
  <p>This is what your form submitted:</p>

  <pre id="output"></pre>

  <p><button id="back">Go Back</button></p>
`;
document.getElementById('back').addEventListener('click', () => window.history.back());

const formData = JSON.parse(document.getElementById('echo').innerHTML);
console.log(formData);

var formDataStr = JSON.stringify(formData, undefined, 4);
output(syntaxHighlight(formDataStr));
