import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';

import { User } from '../_interface/auth.interface';

import Swal from 'sweetalert2';

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
      authToken: userData.authToken,
      email: userData.email,
      name: userData.name,
    };
    return this.http.post(environment.apiUrl + '/login', obj).pipe(
      tap((response: any) => {
        const user: User = {
          id: userData.id,
          name: userData.name,
          email: userData.email,
          avatar: userData.photoUrl,
          jwtToken: response.jwttoken,
          authToken: userData.authToken,
        };
        this.handleSuccess(user, response.message);
      }),
      catchError(this.handleError)
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
        this.router.navigate(['/']);
      }
    } catch (e) {
      this.setUserData(null);
    }
  }

  getCardList(status: string = 'pending') {
    return this.http.get(environment.apiUrl+`/data-status?status=${status}`);
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
    this.showLoader('Uploading your image...')
    let url  = `/card-image?front=${is_front}&card_id=${card_id}`;

    if(!is_front) {
      url  = `/card-image?card_id=${card_id}`
    }

    return this.http.post(
      environment.apiUrl + url,
      imagedata
    ).pipe(
      tap((response: any) => {
        Swal.close();
        this.toastSuccess(response.message)
      }),
      catchError(error => {
        Swal.close();
        this.toastError();
        return throwError('Something went wrong!')
      })
    )
  }

  saveCardDetails(data) {
    this.showLoader();
    return this.http.post(environment.apiUrl+`/save-card-details`, data)
    .pipe(
      tap((response: any) => {
        Swal.close();
        if(response.status_code == '400') {
          this.toastError(response.message)
        } else {
          this.toastSuccess(response.message)
        }
      }),
      catchError(error => {
        Swal.close();
        const errMessage = 'Something went wrong';
        this.toastError(errMessage)
        return throwError(errMessage);
      })
    )
  }

  deleteCard(card_id) {
    this.showLoader();
    return this.http.delete(environment.apiUrl+`/delete-card/${card_id}`)
    .pipe(
      tap((response: any) => {
        Swal.close();
        if(response.success) {
          this.toastSuccess(response.message)
        } else {
          this.toastError(response.message)
        }
      }),
      catchError(error => {
        Swal.close();
        this.toastError();
        return throwError('Something went wrong');
      })
      )
  }

  private handleSuccess(user: User, message) {
    this.setUserData(user);
    this.toastSuccess(message);
    this.router.navigate(['/dashboard']);
  }

  private handleError(error) {
    const errMessage = 'Unable to login';
    this.toastError(errMessage);
    this.router.navigate(['/']);
    return throwError(errMessage);
  }

  private showLoader(text:string = 'Processing ...') {
    Swal.fire({
      title: text,
      onBeforeOpen () {
        Swal.showLoading ()
      },
      onAfterClose () {
        Swal.hideLoading()
      },
      allowOutsideClick: false,
      allowEscapeKey: false,
      allowEnterKey: false,
      showConfirmButton: false,
    })
  }

  private toastSuccess(message) {
    Swal.fire({
      position: 'top-end',
      icon: 'success',
      title: message,
      showConfirmButton: false,
      timer: 1700,
    });
  }

  private toastError(message = 'Something went wrong!') {
    Swal.fire({
      position: 'top-end',
      icon: 'error',
      title: message,
      showConfirmButton: false,
      timer: 1700,
    });
  }
}