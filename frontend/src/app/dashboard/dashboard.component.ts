import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import * as $ from 'jquery';
import { Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';
import { DataService } from '../_providers/data.service';
import { FacebookService } from '../_providers/facebook.service';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.less'],
})
export class DashboardComponent implements OnInit, OnDestroy {
  userData: any;
  dropdownList: any = null;
  userSubscription: Subscription;
  dropdownSubscription: Subscription;
  years = [];
  allExpandState = false;
  viewMode = false;
  collectionList: any = [];

  // Card Form
  cardForm: FormGroup;
  cards: FormArray;
  ind = 0;
  imageUrl = environment.apiUrl;

  constructor(
    private fbService: FacebookService,
    private dataService: DataService,
    private router: Router,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    // $('.collapse').collapse()

    //   $("#open-all").click(function(){
    //     console.log("working")
    //     $(".input-arrow").prop("checked", true);
    // });
    $('#side-nav').click(function () {
      $('.side-upload ').toggle(500);
    });

    // Create Year Dropdown
    for (let i = 2021; i > 1969; i--) {
      let str = i.toString();
      this.years.push(i);
    }

    this.cardForm = this.fb.group({
      cards: this.fb.array([]),
    });

    this.userSubscription = this.dataService.userDetails.subscribe((user) => {
      if (user == null) {
        this.router.navigate(['/']);
      }
      this.userData = user;
    });

    if (!this.dataService.formDropDownList) {
      this.dataService.getDropdownList();
      this.dropdownSubscription = this.dataService.dropdown.subscribe(
        (dropdown) => {
          if (!dropdown) {
            // dropdown  is empty
          } else {
            this.dropdownList = dropdown;
            // this.sortKeys();
          }
        }
      );
    } else {
      this.dropdownList = this.dataService.formDropDownList[0];
      // this.sortKeys();
    }

    this.dataService.getCardList().subscribe(
      (response: any) => {
        if (!response.data.length) {
          this.addCard();
          this.allExpandState = true;
        } else {
          this.populateCardDetails(response.data);
        }
      },
      (error) => {
        this.allExpandState = true;
        this.addCard();
      }
    );
  }

  sortKeys() {
    this.dropdownList.card_grade.sort((a, b) => (a.id > b.id) ? -1 : 1);
    this.dropdownList.auto_grade.sort((a, b) => (a.id > b.id) ? -1 : 1);
  }

  logout() {
    this.fbService.logout();
  }

  ngOnDestroy() {
    this.userSubscription.unsubscribe();
    if (this.dropdownSubscription) {
      this.dropdownSubscription.unsubscribe();
    }
  }

  // Form Maniputlation

  createCard(
    card_id = null,
    category = null,
    player_name = '',
    brand_name = '',
    card_number = '',
    certification = null,
    auto_grade = null,
    card_grade = null,
    year = null,
    certification_number = '',
    autographed = false,
    front_image = null,
    back_image = null
  ) {
    this.ind = this.ind + 1;
    return this.fb.group({
      card_id: [card_id],
      form_group: this.fb.group({
        category: [category, Validators.required],
        player_name: [player_name, Validators.required],
        brand_name: [brand_name, Validators.required],
        card_number: [card_number, Validators.required],
        certification: [certification, Validators.required],
        auto_grade: [auto_grade],
        card_grade: [card_grade, Validators.required],
        year: [year, Validators.required],
        certification_number: [certification_number, Validators.required],
        autographed: [autographed],
      }),
      image_group: this.fb.group({
        front_image: [front_image],
        back_image: [back_image],
      }),
    });
  }

  addCard() {
    this.cards = this.cardForm.get('cards') as FormArray;
    this.cards.push(this.createCard());
    this.enableDisableForm(this.cards.length - 1);
  }

  removeCard(index) {
    this.dataService
      .confirmBox('Are you sure want to delete?')
      .then((result) => {
        if (result.isConfirmed) {
          this.cards = this.cardForm.get('cards') as FormArray;
          if (this.cards.at(index).get('card_id').value) {
            this.dataService
              .deleteCard(this.cards.at(index).get('card_id').value)
              .subscribe(
                (response: any) => {
                  if (response.success) {
                    this.cards.removeAt(index);
                  }
                },
                (error) => {}
              );
          } else {
            this.cards.removeAt(index);
          }
        }
      });
  }

  populateCardDetails(cardList) {
    this.cards = this.cardForm.get('cards') as FormArray;
    cardList.forEach((element) => {
      this.cards.push(
        this.createCard(
          element.id,
          element.category,
          element.player_name,
          element.brand_name,
          element.card_number,
          element.certification,
          element.auto_grade,
          element.card_grade,
          element.year,
          element.certification_number,
          element.autographed,
          element.front_thumbnail,
          element.back_thumbnail
        )
      );
      this.enableDisableForm(this.cards.length - 1);
    });
  }

  enableDisableForm(index) {
    this.cards = this.cardForm.get('cards') as FormArray;
    const card = this.cards.at(index);
    if (
      card.get(['image_group', 'back_image']).value != null &&
      card.get(['image_group', 'front_image']).value != null
    ) {
      this.cards.at(index).get('form_group').enable();
    } else {
      // this.cards.at(index).get('form_group').disable();
    }
  }

  // ImageUpload

  imageUploaded($event, index, is_front) {

    if(!$event.target.files.length) { return }
    const fromData = new FormData();
    fromData.append('image', $event.target.files[0]);

    this.cards = this.cardForm.get('cards') as FormArray;
    const card_id = this.cards.at(index).get('card_id').value;

    this.dataService.uploadImage(fromData, is_front, card_id).subscribe(
      (response: any) => {
        if (is_front) {
          this.cards.at(index).get('image_group').patchValue({
            front_image: response.data.front_thumbnail,
          });
        } else {
          this.cards.at(index).get('image_group').patchValue({
            back_image: response.data.back_thumbnail,
          });
        }
        this.cards.at(index).patchValue({
          card_id: response.data.id,
        });
        this.enableDisableForm(index);
      },
      (error) => {}
    );
  }

  updateAutographed($event, index, is_enable) {
    this.cards = this.cardForm.get('cards') as FormArray;
    this.cards.at(index).get('form_group').patchValue({
      autographed: is_enable,
    });
  }

  updateCardData(index) {
    this.cards = this.cardForm.get('cards') as FormArray;
    const card_det = this.cards.at(index);
    const cardData = card_det.get('form_group').value;
    cardData['autographed'] = card_det.get(['form_group', 'autographed']).value ? true : false;

    if(card_det.get('card_id').value) {
      cardData['card_id'] = card_det.get('card_id').value;
    }

    if(!!cardData.auto_grade) {
      cardData['auto_grade'] = card_det.get(['form_group','auto_grade']).value;
    } else {
      delete cardData.auto_grade
    }

    if(!card_det.get(['image_group','front_image']).value || !card_det.get(['image_group','back_image']).value ) {
      this.dataService.confirmBox('Your images are not uploaded yet! Are you sure you want to continue ?')
      .then(result => {
        if (result.isConfirmed) {
          this.saveCardDetails(index, cardData)
          }
      });
      return
    }
    this.saveCardDetails(index, cardData)
  }

  saveCardDetails(index, cardData) {
    this.dataService.saveCardDetails(cardData).subscribe(
      (response) => {
        if (response.success == 'False') {
          return;
        }
        this.cards.removeAt(index);
      },
      (error) => {}
    );
  }

  // fetchCollections() {
  //   this.dataService.getCardList('done').subscribe(
  //     (response: any) => {
  //       this.collectionList = response.data;
  //       this.collectionList.forEach((element) => {
  //         element['category'] = this.findCategoryLabel(element.category);
  //         element['certification'] = this.findCertificationLabel(
  //           element.certification
  //         );
  //         element['card_grade'] = this.findCardGradeLabel(element.card_grade);
  //         element['auto_grade'] = this.findAutoGradeLabel(element.auto_grade);
  //       });
  //     },
  //     (error) => {
  //       this.collectionList = [];
  //     }
  //   );
  // }

  // findCategoryLabel(id) {
  //   const label = this.dropdownList.category.find((x) => x.id == id);
  //   return label.category_name;
  // }

  // findCertificationLabel(id) {
  //   const label = this.dropdownList.certification.find((x) => x.id == id);
  //   return label.certificate_name;
  // }

  // findCardGradeLabel(id) {
  //   const label = this.dropdownList.card_grade.find((x) => x.id == id);
  //   return label.card_grade_name;
  // }

  // findAutoGradeLabel(id) {
  //   const label = this.dropdownList.auto_grade.find((x) => x.id == id);
  //   return label.grade_name;
  // }

  deleteCard(index) {
    this.dataService.deleteCard(this.collectionList[index].id).subscribe(
      (response: any) => {
        if (response.success) {
          this.collectionList.splice(index, 1);
        }
      },
      (error) => {}
    );
  }

  changeImage(index, type='front') {
    const id = `image_upload_${type}${index}`;
    const fileInput = document.getElementById(id);
    fileInput.click();
  }

  sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
    });
  }
}
