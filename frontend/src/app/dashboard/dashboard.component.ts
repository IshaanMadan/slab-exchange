import { Component, OnInit } from '@angular/core';
import * as $ from "jquery";
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less']
})
export class DashboardComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    // $('.collapse').collapse()
    $("#open-all").click(function(){
      console.log("working")
      $(".input-arrow").prop("checked", true);
  });
  $("#side-nav").click(function(){
    $(".side-upload ").toggle(500)
  });
  }
 
  

}
