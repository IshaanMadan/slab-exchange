import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DataService } from '../_providers/data.service';
import { FacebookService } from '../_providers/facebook.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit, OnDestroy {

  showPassword = false;
  loginForm: FormGroup
  signUpForm: FormGroup

  constructor(
    private fb: FormBuilder,
    private dataService: DataService,
    private fbService: FacebookService
  ) { }

  ngOnInit(): void {
    this.signUpForm = this.fb.group({
      firstName: ['',Validators.compose([Validators.required])],
      lastName: ['',Validators.compose([Validators.required])],
      email: ['',Validators.compose([Validators.required,Validators.pattern(/^\s*(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9!#$%&'*+-/=?^_`{|}~;]+\.)+[a-zA-Z]{2,}))\s*$/)])],
      password: ['', Validators.compose([Validators.required,Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)])],
      agreetoTerms: [false, Validators.requiredTrue]
    })
    this.loginForm = this.fb.group({
      email: ['',Validators.compose([Validators.required,Validators.pattern(/^\s*(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9!#$%&'*+-/=?^_`{|}~;]+\.)+[a-zA-Z]{2,}))\s*$/)])],
      password: ['', Validators.compose([Validators.required,Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)])],
    })
  }

  loginFB() {
    this.fbService.loginViaFacebook();
  }

  loginGoogle() {
    this.fbService.loginViaGoogle();
  }

  ngOnDestroy() {

  }

  changedTab($event) {
    this.showPassword = false;
    this.loginForm.reset();
    this.signUpForm.reset();
  }

  loginViaEmail() {
    const userData = this.loginForm.getRawValue()
    // console.log('Login ', this.loginForm.getRawValue());
    this.dataService.login(userData)
    .subscribe(response => {
      // console.log('Response ', response)
    })
  }

  signupViaEmail() {
    // console.log('signup ', this.signUpForm.getRawValue());
    const userData = this.signUpForm.getRawValue()

    this.dataService.signup(userData)
    .subscribe((response) => { }, (error) => { })
  }

}
