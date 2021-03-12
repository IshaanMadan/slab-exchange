import { Injectable } from '@angular/core';
import {
    HttpInterceptor,
    HttpRequest,
    HttpResponse,
    HttpHandler,
    HttpEvent,
    HttpErrorResponse
} from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

@Injectable()
export class HttpConfigInterceptor implements HttpInterceptor {
    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
      let token = null;
      try {
        let userData = JSON.parse(localStorage.getItem('user'))
        token = userData.jwtToken
      } catch(e) {
        token = null
      }

      if (token) {
          request = request.clone({ headers: request.headers.set('Authorization', 'Bearer ' + token) });
      }

      if (!request.headers.has('Content-Type') && !request.url.includes('card-image')) {
          request = request.clone({ headers: request.headers.set('Content-Type', 'application/json') });
      }

      request = request.clone({ headers: request.headers.set('Accept', 'application/json') });

      return next.handle(request).pipe(
          map((event: HttpEvent<any>) => {
              if (event instanceof HttpResponse) { }
              return event;
          }));
  }

}
