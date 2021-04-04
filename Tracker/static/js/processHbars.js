var template = document.getElementById('glob-template').innerHTML;
var renderGlob = Handlebars.compile(template);
document.getElementById('glob').innerHTML = renderGlob({
  globdata: respfile.Global,
});

