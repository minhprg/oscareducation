// var casper = require('casper').create();

casper.start('http://127.0.0.1:8000/accounts/usernamelogin/');

casper.then(function() {
    this.fill('form#login-form', {
        'username': 'PeterParker'
    }, true);
});

casper.then(function() {
    this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/accounts/passwordlogin/");
});

casper.then(function() {
    this.fill('form#login-form', {
        'password': 'sjS3bejvep$'
    }, true);
});

casper.then(function() {
    setTimeout( function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/professor/dashboard/");
    }, 1000);
});

casper.then(function() {
    // Click on 1st result link
    this.click('img[class="buttonimg"]');
});

casper.run();

casper.then(function() {
    console.log('clicked ok2, new location is ' + this.getCurrentUrl());
});

casper.then(function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/professor/education/");
});
