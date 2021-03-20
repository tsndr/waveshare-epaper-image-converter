#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include "imagedata.h"
#include <stdlib.h>

void setup() {
  DEV_Module_Init();

  printf("e-Paper Init and Clear...\r\n");
  EPD_4IN2B_V2_Init();
  EPD_4IN2B_V2_Clear();

  //Create a new image cache named IMAGE_BW and fill it with white
  UBYTE *BlackImage, *RYImage; // Red or Yellow
  UWORD Imagesize = ((EPD_4IN2B_V2_WIDTH % 8 == 0) ? (EPD_4IN2B_V2_WIDTH / 8 ) : (EPD_4IN2B_V2_WIDTH / 8 + 1)) * EPD_4IN2B_V2_HEIGHT;
  if ((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    printf("Failed to apply for black memory...\r\n");
    while(1);
  }
  if ((RYImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    printf("Failed to apply for red memory...\r\n");
    while(1);
  }
  printf("NewImage:BlackImage and RYImage\r\n");
  Paint_NewImage(BlackImage, EPD_4IN2B_V2_WIDTH, EPD_4IN2B_V2_HEIGHT, 180, WHITE);
  Paint_NewImage(RYImage, EPD_4IN2B_V2_WIDTH, EPD_4IN2B_V2_HEIGHT, 180, WHITE);

  //Select Image
  Paint_SelectImage(BlackImage);
  Paint_Clear(WHITE);
  Paint_SelectImage(RYImage);
  Paint_Clear(WHITE);

  printf("show image for array\r\n");
  EPD_4IN2B_V2_Display(gImage_4in2bc_b, gImage_4in2bc_ry);

  printf("Goto Sleep...\r\n");
  EPD_4IN2B_V2_Sleep();
  free(BlackImage);
  free(RYImage);
  BlackImage = NULL;
  RYImage = NULL;
}

void loop() {}
