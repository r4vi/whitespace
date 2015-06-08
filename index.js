var Metalsmith = require('metalsmith');
var drafts = require('metalsmith-drafts');
var markdown = require('metalsmith-markdown');
var permalinks = require('metalsmith-permalinks');
var templates = require('metalsmith-templates');
var _static = require('metalsmith-static');
var writemetadata = require('metalsmith-writemetadata');
var watch = require('metalsmith-watch');
var serve = require('metalsmith-serve');

var ms = Metalsmith(__dirname)
  .source('./content/post')
  .use(permalinks('post/:title'))
  .use(console.log)
  .use(markdown({
      smartypants: true,
      gfm: true,
      tables: true,
      pattern: 'post/**.md'
  }))
  .use(templates(
    {
       engine: 'jade',
       directory: './templates',
       inPlace: false,
       default: 'flatpage.jade'
      }
  )) 
  .use(drafts())
  .use(_static({src: './static/', dest: './static/'}))
  .use(writemetadata())
//  .use(watch())
//  .use(serve())
ms.build(function(err) {
    if (err) throw err;
  });
