casper.start('http://127.0.0.1:8000/accounts/usernamelogin/');


//introduce the username
casper.then(function() {
    this.fill('form#login-form', {
        'username':    'simon'
    }, true);
})
//wait for the chargement of the page
.wait(1000, function() {
    })
.then(function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/accounts/passwordlogin/");
})
//introduce the password
.then(function() {
    this.fill('form#login-form', {
        'password':    'simon'
    }, true);
})
//wait for the chargement of the page
.wait(1000, function() {
    })
//verif if the user is login
.then(function() {
        this.test.assertEquals(this.getCurrentUrl(), "http://127.0.0.1:8000/professor/dashboard/");
})
//click on the button on the page
.then(function() {
    this.click('img[class="buttonimg"]');
})


//open the page for create algrebraic expression
.thenOpen('http://127.0.0.1:8000/algebra/exercice/creation')
//test of a valid submission
.then(function() {
    this.fill('form.formgroup', {
	'exercice_level' : '1',
        'leftSide':    'x^2',
	'rightSide' :  '2*x',
	'solution' : 'x^2-2*x=0'
    }, true);
})
.then(function(){
    this.test.assertHttpStatus(200, 'Check server returned 200 => the expression is correct');
})

//test the submission of an invalid form
.then(function() {
    this.fill('form.formgroup', {
	'exercice_level' : '1',
        'leftSide':    'xdfdf2',
	'rightSide' :  '2***x',
	'solution' : 'x^2-2*x=0'
    }, true);
})
.then(function(){
    this.test.assertHttpStatus(422, 'Check server returned 422 => bad format');
})

//test the submission of a invalid solution
.then(function() {
    this.fill('form.formgroup', {
	'exercice_level' : '1',
        'leftSide':    'x^2',
	'rightSide' :  '2*x',
	'solution' : 'x^2-3*x=0'
    }, true);
})
.then(function(){
    this.test.assertHttpStatus(422, 'Check server returned 422 => bad solution');
})
.run();

// this.echo(this.currentHTTPStatus);


