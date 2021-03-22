import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { SocialAuthService } from "angularx-social-login";
import { FacebookLoginProvider, GoogleLoginProvider } from "angularx-social-login";
import { DataService } from './data.service';


@Injectable({
  providedIn: 'root'
})
export class FacebookService {
  loginVia = '';
  constructor(
    private router: Router,
    private authService: SocialAuthService,
    private dataService: DataService
  ) {
    this.authService.authState.subscribe((user) => {
      if(user != null) {
        this.dataService.login(user)
        .subscribe(response => { }, error => { });

        // mock test
        // this.dataService.setUserData(user);
        // this.router.navigate(['/dashboard']);
      } else {
        this.router.navigate(['/']);
      }
    });
  }

  loginViaFacebook() {
    this.loginVia = 'FACEBOOK';
    this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  loginViaGoogle() {
    this.loginVia = 'GOOGLE';
    this.authService.signIn(GoogleLoginProvider.PROVIDER_ID);
  }

  logout() {
    this.authService.signOut();
    this.dataService.setUserData(null);
    localStorage.removeItem('user');
  }

}
