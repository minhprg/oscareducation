casper.start('http://127.0.0.1:8000/accounts/usernamelogin/');

casper.then(function() {
    this.fill('form#login-form', {
        'username':    'simon'
    }, true);
    console.log('clicked 1 ');
})
.wait(1000, function() {
        this.echo("I've waited for a second.");
    })
.then(function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/accounts/passwordlogin/");
})
.then(function() {
    this.fill('form#login-form', {
        'password':    'simon'
    }, true);
    console.log('clicked 2 ');
})
.wait(1000, function() {
        this.echo("I've waited for a second.");
    })
.then(function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/professor/dashboard/");
})
.then(function() {
    // Click on 1st result link
    this.click('img[class="buttonimg"]');
    console.log('clicked 3 ');
})
.run();

casper.then(function() {
    console.log('clicked ok2, new location is ' + this.getCurrentUrl());
});
casper.then(function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/professor/education/");
});
