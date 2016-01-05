// Karma configuration
// Generated on Wed Nov 25 2015 18:41:20 GMT+0100 (CET)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'hoodpub/static/hoodpub/js/bower_components/jquery/dist/jquery.min.js',
      'hoodpub/static/hoodpub/js/bower_components/bootstrap/dist/js/bootstrap.min.js',
      'hoodpub/static/hoodpub/js/bower_components/angular/angular.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-cookies/angular-cookies.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-resource/angular-resource.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-route/angular-route.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-jwt/dist/angular-jwt.min.js',
      'hoodpub/static/hoodpub/js/bower_components/spin.js/spin.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-google-analytics/dist/angular-google-analytics.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-spinner/angular-spinner.js',
      'hoodpub/static/hoodpub/js/bower_components/angular-mocks/angular-mocks.js',
      'hoodpub/static/hoodpub/js/bower_components/readmore-js/readmore.js',
      'hoodpub/js/graph/vivagraph.js',
      'hoodpub/static/hoodpub/js/ng-infinite-scroll.js',
      'hoodpub/static/hoodpub/js/angular-relative-date.js',
      'hoodpub/static/hoodpub/js/ui-bootstrap-custom-build/ui-bootstrap-custom-tpls-0.14.3.js',
      'hoodpub/static/hoodpub/js/services.js',
      'hoodpub/static/hoodpub/js/controllers.js',
      'hoodpub/static/hoodpub/js/app.js',
      'hoodpub/static/hoodpub/js/*.js',
      'hoodpub/static/hoodpub/test/spec/*.js',
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_DEBUG,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false,

    // Concurrency level
    // how many browser should be started simultanous
    concurrency: Infinity
  })
}
