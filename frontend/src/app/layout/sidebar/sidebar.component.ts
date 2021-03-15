import { Component, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.less']
})
export class SidebarComponent implements OnInit {
  currentUrl = '/dashboard'
  constructor(
    private router: Router,
  ) {
    this.router.events.subscribe(routes => {
      if(routes instanceof NavigationEnd) {
        this.currentUrl = routes.url;
        // console.log('current', this.currentUrl)
      }
    })
  }

  ngOnInit(): void {
  }

  navigateTo(path = 'dashboard') {
    this.router.navigate([`/${path}`])
  }



}
