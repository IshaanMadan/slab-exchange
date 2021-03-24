import { Component, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { DataService } from 'src/app/_providers/data.service';
import { FacebookService } from 'src/app/_providers/facebook.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.less'],
})
export class HeaderComponent implements OnInit {
  userSubscription: Subscription;
  userData: any;
  public innerWidth: any;
  userName;

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.innerWidth = window.innerWidth;
    this.nameResize();
  }

  constructor(
    private fbService: FacebookService,
    private dataService: DataService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userSubscription = this.dataService.userDetails.subscribe((user) => {
      if (user == null) {
        this.router.navigate(['/']);
      }
      this.userData = user;
    });
    this.innerWidth = window.innerWidth;
    this.nameResize();
  }

  logout() {
    this.fbService.logout();
  }

  nameResize() {
    this.userName =
      this.innerWidth < 576
        ? this.userData.name.split(' ')[0]
        : this.userData.name;
  }
}
