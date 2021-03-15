import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { data } from 'jquery';
import { DataService } from './_providers/data.service';

declare var FB:any
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  title = 'Slab Exchange';
  showHeader$ = false;
  showSidebar$ = false;

  constructor(
    private dataService: DataService
    ) {
    dataService.autoLogin();
    dataService.userDetails.subscribe(user => {
      if(user!=null) {
        this.showHeader$ = true;
        this.showSidebar$ = true;
      } else {
        this.showHeader$ = false;
        this.showSidebar$ = false;
      }
    })
  }


}
