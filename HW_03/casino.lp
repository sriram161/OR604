\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  1200 xfloor_1_NIB + 3100 xfloor_1_DIR + 3000 xfloor_1_DOR
   + 550 xfloor_1_GRP + 2000 xfloor_1_HDD + 2000 xfloor_1_MOL
   + 2500 xfloor_1_BLJ + 1200 xfloor_2_NIB + 3100 xfloor_2_DIR
   + 3000 xfloor_2_DOR + 550 xfloor_2_GRP + 2000 xfloor_2_HDD
   + 2000 xfloor_2_MOL + 2500 xfloor_2_BLJ + 1200 xfloor_3_NIB
   + 3100 xfloor_3_DIR + 3000 xfloor_3_DOR + 550 xfloor_3_GRP
   + 2000 xfloor_3_HDD + 2000 xfloor_3_MOL + 2500 xfloor_3_BLJ
   + 1200 xfloor_4_NIB + 3100 xfloor_4_DIR + 3000 xfloor_4_DOR
   + 550 xfloor_4_GRP + 2000 xfloor_4_HDD + 2000 xfloor_4_MOL
   + 2500 xfloor_4_BLJ
Subject To
 floor_1: 2 xfloor_1_NIB + 2.5 xfloor_1_DIR + 6 xfloor_1_DOR
   + 2.75 xfloor_1_GRP + 3.5 xfloor_1_HDD + 4 xfloor_1_MOL
   + 2.75 xfloor_1_BLJ <= 750
 floor_2: 2 xfloor_2_NIB + 2.5 xfloor_2_DIR + 6 xfloor_2_DOR
   + 2.75 xfloor_2_GRP + 3.5 xfloor_2_HDD + 4 xfloor_2_MOL
   + 2.75 xfloor_2_BLJ <= 1000
 floor_3: 2 xfloor_3_NIB + 2.5 xfloor_3_DIR + 6 xfloor_3_DOR
   + 2.75 xfloor_3_GRP + 3.5 xfloor_3_HDD + 4 xfloor_3_MOL
   + 2.75 xfloor_3_BLJ <= 550
 floor_4: 2 xfloor_4_NIB + 2.5 xfloor_4_DIR + 6 xfloor_4_DOR
   + 2.75 xfloor_4_GRP + 3.5 xfloor_4_HDD + 4 xfloor_4_MOL
   + 2.75 xfloor_4_BLJ <= 700
 hours: 0.67 xfloor_1_NIB + xfloor_1_DIR + 2 xfloor_1_DOR
   + 1.1 xfloor_1_GRP + 0.67 xfloor_1_HDD + 0.5 xfloor_1_MOL
   + 0.75 xfloor_1_BLJ + 0.67 xfloor_2_NIB + xfloor_2_DIR + 2 xfloor_2_DOR
   + 1.1 xfloor_2_GRP + 0.67 xfloor_2_HDD + 0.5 xfloor_2_MOL
   + 0.75 xfloor_2_BLJ + 0.67 xfloor_3_NIB + xfloor_3_DIR + 2 xfloor_3_DOR
   + 1.1 xfloor_3_GRP + 0.67 xfloor_3_HDD + 0.5 xfloor_3_MOL
   + 0.75 xfloor_3_BLJ + 0.67 xfloor_4_NIB + xfloor_4_DIR + 2 xfloor_4_DOR
   + 1.1 xfloor_4_GRP + 0.67 xfloor_4_HDD + 0.5 xfloor_4_MOL
   + 0.75 xfloor_4_BLJ <= 835
 handon_NIB: xfloor_1_NIB + xfloor_2_NIB + xfloor_3_NIB + xfloor_4_NIB
   <= 200
 handon_DIR: xfloor_1_DIR + xfloor_2_DIR + xfloor_3_DIR + xfloor_4_DIR
   <= 150
 handon_DOR: xfloor_1_DOR + xfloor_2_DOR + xfloor_3_DOR + xfloor_4_DOR
   <= 100
 handon_GRP: xfloor_1_GRP + xfloor_2_GRP + xfloor_3_GRP + xfloor_4_GRP
   <= 250
 handon_HDD: xfloor_1_HDD + xfloor_2_HDD + xfloor_3_HDD + xfloor_4_HDD
   <= 125
 handon_MOL: xfloor_1_MOL + xfloor_2_MOL + xfloor_3_MOL + xfloor_4_MOL
   <= 100
 handon_BLJ: xfloor_1_BLJ + xfloor_2_BLJ + xfloor_3_BLJ + xfloor_4_BLJ
   <= 250
Bounds
End
