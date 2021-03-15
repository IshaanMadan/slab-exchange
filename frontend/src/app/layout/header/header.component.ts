import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { DataService } from 'src/app/_providers/data.service';
import { FacebookService } from 'src/app/_providers/facebook.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.less']
})
export class HeaderComponent implements OnInit {

  userSubscription: Subscription
  userData: any;

  constructor(
    private fbService: FacebookService,
    private dataService: DataService,
    private router: Router
    ) { }

  ngOnInit(): void {
    this.userSubscription = this.dataService.userDetails.subscribe(user => {
      if(user == null) {
        this.router.navigate(['/'])
      }
      this.userData = user;
    });
  }

  logout() {
    this.fbService.logout();
  }

}
