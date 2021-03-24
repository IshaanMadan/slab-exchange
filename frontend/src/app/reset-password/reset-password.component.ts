import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ValidationErrors,
  Validators,
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from '../_providers/data.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.less'],
})
export class ResetPasswordComponent implements OnInit {
  resetPasswordForm: FormGroup;

  showPassword = false;
  showConfPassword = false;
  token: any;

  constructor(
    private fb: FormBuilder,
    private dataService: DataService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.token = this.route.snapshot.queryParamMap.get('token');
    // console.log(this.token);
    if (!this.token) {
      this.router.navigate(['']);
    }
    this.initForm();
  }

  initForm() {
    this.resetPasswordForm = this.fb.group({
      password: [
        '',
        Validators.compose([
          Validators.required,
          Validators.pattern(
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
          ),
        ]),
      ],
      confirm_password: [
        '',
        [
          Validators.required,
          // Validators.pattern(
          //   /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/
          // ),
          this.matchValues('password'),
        ],
      ],
    });
  }

  matchValues(
    matchTo: string // name of the control to match to
  ): (AbstractControl) => ValidationErrors | null {
    return (control: AbstractControl): ValidationErrors | null => {
      return !!control.parent &&
        !!control.parent.value &&
        control.value === control.parent.controls[matchTo].value
        ? null
        : { isMatching: false };
    };
  }

  submit() {
    if (this.token) {
      this.resetPasswordForm.value['token'] = this.token;
      // console.log(this.resetPasswordForm.value);

      this.dataService.resetPassword(this.resetPasswordForm).subscribe(
        (res) => {},
        (err) => {}
      );
    } else {
      this.router.navigate(['']);
    }
  }
}
