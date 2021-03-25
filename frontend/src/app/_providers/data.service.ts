import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

import { User } from '../_interface/auth.interface';

import Swal from 'sweetalert2';
import { FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private _userDetails = new BehaviorSubject(null);
  public userDetails = this._userDetails.asObservable();

  private _dropdownList = new BehaviorSubject(null);
  public dropdown = this._dropdownList.asObservable();

  formDropDownList: any = null;

  constructor(private http: HttpClient, private router: Router) {}

  login(userData) {
    const obj = {
      email: userData.email,
    };
    if ('provider' in userData) {
      obj['authToken'] = userData.authToken;
      obj['name'] = userData.name;
      obj['login_type'] = userData.provider;
    } else {
      obj['password'] = userData.password;
      obj['login_type'] = 'EMAIL';
    }
    this.showLoader();
    return this.http.post(environment.apiUrl + '/login', obj).pipe(
      tap((response: any) => {
        Swal.close();

        const user: User = {
          id: userData.id,
          // name: userData.name,
          // email: userData.email,
          name: response.name,
          email: userData.email,
          // avatar: userData.photoUrl,
          jwtToken: response.jwttoken,
          authToken: userData.authToken,
        };

        this.handleSuccess(user, response.message);
      }),
      catchError((error) => {
        Swal.close();
        // const errMessage = 'Unable to login';
        this.toastError(error?.error.message);
        this.router.navigate(['/']);
        return throwError(error?.error.message);
      })
    );
  }

  signup(userData) {
    const obj = {
      first_name: userData.firstName,
      last_name: userData.lastName,
      email: userData.email,
      password: userData.password,
    };
    this.showLoader();
    return this.http.post(environment.apiUrl + `/user-signup`, obj).pipe(
      tap((response: any) => {
        Swal.close();
        // const user: User = {
        //   id: userData.id,
        //   name: userData.firstName + ' ' + userData.lastName,
        //   email: userData.email,
        //   // avatar: userData.photoUrl,
        //   jwtToken: response.jwttoken,
        //   authToken: userData.authToken,
        // };
        // this.handleSuccess(user, response.message);
        if(response.success === "True"){
          this.toastSuccess(response.message);
          this.router.navigate(['/']);
        }else{
          this.toastError(response.message);
          this.router.navigate(['/']);
        }

      }),
      catchError((error) => {
        Swal.close();
        const errMessage = 'Unable to signup';
        this.toastError(errMessage);
        this.router.navigate(['/']);
        return throwError(errMessage);
      })
    );
  }

  setUserData(userData) {
    this._userDetails.next(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  }

  autoLogin() {
    try {
      const user = JSON.parse(localStorage.getItem('user'));
      if (user != null) {
        this.setUserData(user);
        this.router.navigate(['/dashboard']);
      } else {
        // this.router.navigate(['/']);
      }
    } catch (e) {
      this.setUserData(null);
    }
    // console.log(this.router.url)
  }

  getCardList(status: string = 'pending') {
    return this.http.get(
      environment.apiUrl + `/card-data-status?status=${status}`
    );
  }

  getDropdownList() {
    this.http.get(environment.apiUrl + '/get-form-list').subscribe(
      (response: any) => {
        this.setDropdown(response.data[0]);
        this.formDropDownList = response.data;
      },
      (error) => {
        this.setDropdown(null);
      }
    );
  }

  setDropdown(data) {
    this._dropdownList.next(data);
  }

  uploadImage(imagedata, is_front, card_id) {
    let url = `/card-image?`;
    if (card_id) {
      url = url + `card_id=${card_id}&`;
    }
    if (is_front) {
      url = url + `front=${is_front}`;
    }
    this.showLoader('Uploading your image...');
    return this.http.post(environment.apiUrl + url, imagedata).pipe(
      tap((response: any) => {
        Swal.close();
        this.toastSuccess(response.message);
      }),
      catchError((error) => {
        Swal.close();
        this.toastError();
        return throwError('Something went wrong!');
      })
    );
  }

  saveCardDetails(data) {
    this.showLoader();
    return this.http.post(environment.apiUrl + `/save-card-details`, data).pipe(
      tap((response: any) => {
        Swal.close();
        if (response.status_code == '400') {
          this.toastError(response.message);
        } else {
          this.toastSuccess(response.message);
        }
      }),
      catchError((error) => {
        Swal.close();
        const errMessage = 'Something went wrong';
        this.toastError(errMessage);
        return throwError(errMessage);
      })
    );
  }

  deleteCard(card_id) {
    this.showLoader();
    return this.http
      .delete(environment.apiUrl + `/delete-card/${card_id}`)
      .pipe(
        tap((response: any) => {
          Swal.close();
          if (response.success) {
            this.toastSuccess(response.message);
          } else {
            this.toastError(response.message);
          }
        }),
        catchError((error) => {
          Swal.close();
          this.toastError();
          return throwError('Something went wrong');
        })
      );
  }

  private handleSuccess(user: User, message) {
    this.setUserData(user);
    this.toastSuccess(message);
    this.router.navigate(['/dashboard']);
  }

  private handleError(error) {
    const errMessage = 'Unable to login';
    this.toastError();
    this.router.navigate(['/']);
    return throwError(errMessage);
  }

  confirmBox(
    confirmation_text = 'Are you sure want to continue?'
  ): Promise<any> {
    return Swal.fire({
      title: confirmation_text,
      // text: 'You will not be able to recover this file!',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes',
      cancelButtonText: 'No',
    });
  }

  private showLoader(text: string = 'Processing ...') {
    Swal.fire({
      title: text,
      onBeforeOpen() {
        Swal.showLoading();
      },
      onAfterClose() {
        Swal.hideLoading();
      },
      allowOutsideClick: false,
      allowEscapeKey: false,
      allowEnterKey: false,
      showConfirmButton: false,
    });
  }

  private toastSuccess(message) {
    Swal.fire({
      position: 'top',
      icon: 'success',
      title: message,
      showConfirmButton: false,
      timer: 1700,
    });
  }

  private toastError(message = 'Something went wrong!') {
    Swal.fire({
      position: 'top',
      icon: 'error',
      title: message,
      showConfirmButton: false,
      timer: 1700,
    });
  }

  verifyAccount(token) {
    this.showLoader();
    return this.http.post(environment.apiUrl + '/verify-token', token).pipe(
      tap((response: any) => {
        Swal.close();
        console.log(response);
        this.toastSuccess(response.message);
        this.router.navigate(['/']);
      }),
      catchError((error) => {
        Swal.close();
        const errMessage = 'Somthing Went Wrong';
        this.toastError(errMessage);
        this.router.navigate(['/']);
        return throwError(errMessage);
      })
    );
  }

  async forgotPassModal(loginForm) {
    const { value: email } = await Swal.fire({
      title: 'Forgot Password?',
      html: `<p>If you have forgotten your password you can reset it here.
       Please enter your registered email address below.</p>
      `,
      input: 'email',
      inputPlaceholder: 'Email Address',
      confirmButtonText: 'Submit',
    });

    if (email) {
      // Swal.fire('Entered email: ' + email)
      this.forgotPassword(loginForm, { email: email }).subscribe();
    }
  }

  forgotPassword(loginForm:FormGroup ,data) {
    this.showLoader();
    console.log(data);
    return this.http.post(environment.apiUrl + '/forget-password', data).pipe(
      tap((response: any) => {
        Swal.close();
        this.toastSuccess(response.message);
        loginForm.reset()
        this.router.navigate(['/']);
      }),
      catchError((error) => {
        Swal.close();
        // const errMessage = 'Something Went Wrong';
        this.toastError(error?.error.message);
        loginForm.reset()
        this.router.navigate(['/']);
        return throwError(error?.error.message);
      })
    );
  }

  resetPassword(data: FormGroup) {
    this.showLoader();
    return this.http
      .post(environment.apiUrl + '/reset-password', data.value)
      .pipe(
        tap((response: any) => {
          Swal.close();
          data.reset();
          this.toastSuccess(response.message);
          this.router.navigate(['/']);
        }),
        catchError((error) => {
          Swal.close();
          data.reset();
          // const errMessage = 'Something Went Wrong';
          this.toastError(error?.error.message);
          // this.router.navigate(['/']);
          return throwError(error?.error.message);
        })
      );
  }
}
