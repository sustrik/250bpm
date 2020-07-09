var fs = require('fs');

for (var b = 1; b < 161; b++) {
  fname = '' + b + '/blog.html'
  console.log(fname)

  var html = fs.readFileSync(fname, 'utf8')

  var TurndownService = require('turndown')
  var turndownService = new TurndownService()
  var md = turndownService.turndown(html)

  var idx = md.indexOf("[Create account]")
  md = md.substring(idx)

  var idx = md.indexOf("[Show Comments]")
  md = md.substring(0, idx)

  var lines = md.split('\n');
  md = ''
  for(i = 1; i < lines.length; i++) {
     if(lines[i].startsWith("**Next:**")) continue
     if(lines[i].startsWith("**Previous:**")) continue
     md += lines[i] + "\n"
  }
  md = "# " + md.trim()

  fs.writeFileSync('' + b + '/blog.md', md)
}
