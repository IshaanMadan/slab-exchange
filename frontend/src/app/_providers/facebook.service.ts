import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { SocialAuthService } from "angularx-social-login";
import { FacebookLoginProvider } from "angularx-social-login";
import { DataService } from './data.service';


@Injectable({
  providedIn: 'root'
})
export class FacebookService {

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

  login() {
    this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  logout() {
    this.authService.signOut();
    this.dataService.setUserData(null);
    localStorage.removeItem('user');
  }

}
