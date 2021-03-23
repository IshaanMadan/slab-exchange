import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from '../_providers/data.service';

@Component({
  selector: 'app-verify-user',
  templateUrl: './verify-user.component.html',
  styleUrls: ['./verify-user.component.less'],
})
export class VerifyUserComponent implements OnInit {
  token;

  constructor(
    private route: ActivatedRoute,
    private service: DataService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.token = this.route.snapshot.queryParamMap.get('token');
    // console.log(this.token);
    if (this.token) {
      this.activateAcc();
    } else {
      this.router.navigate([''])
    }
  }

  activateAcc() {
    this.service.verifyAccount({ token: this.token }).subscribe((response) => {
      // console.log('Response ', response)
    });
  }
}
