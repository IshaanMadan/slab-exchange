import { Component, OnInit, OnDestroy } from '@angular/core';
import { FacebookService } from '../_providers/facebook.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.less']
})
export class LoginComponent implements OnInit, OnDestroy {

  constructor(
    private fbService: FacebookService
  ) { }

  ngOnInit(): void {
  }

  login() {
    this.fbService.login();
  }

  ngOnDestroy() {

  }

}
