import { Component } from '@angular/core';
import { DataService } from './_providers/data.service';

declare var FB:any
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  title = 'Slab Exchange';

  constructor(private dataService: DataService) {
    dataService.autoLogin();
  }
}
