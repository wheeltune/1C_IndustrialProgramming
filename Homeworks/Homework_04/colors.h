unsigned char colors[256][3] = {{0, 0, 0}, {15, 40, 63}, {22, 50, 75}, {27, 57, 83}, {31, 63, 90}, {35, 68, 95}, {39, 73, 99}, {42, 76, 103}, {45, 80, 107}, {47, 83, 110}, {50, 86, 113}, {52, 89, 116}, {55, 92, 118}, {57, 94, 121}, {59, 96, 123}, {61, 99, 125}, {63, 101, 127}, {65, 103, 129}, {67, 105, 131}, {69, 107, 133}, {71, 109, 134}, {73, 110, 136}, {74, 112, 138}, {76, 114, 139}, {78, 115, 141}, {79, 117, 142}, {81, 119, 144}, {82, 120, 145}, {84, 122, 146}, {85, 123, 148}, {87, 124, 149}, {88, 126, 150}, {90, 127, 151}, {91, 128, 152}, {93, 130, 154}, {94, 131, 155}, {95, 132, 156}, {97, 133, 157}, {98, 135, 158}, {99, 136, 159}, {100, 137, 160}, {102, 138, 161}, {103, 139, 162}, {104, 140, 163}, {105, 141, 164}, {107, 143, 165}, {108, 144, 166}, {109, 145, 167}, {110, 146, 167}, {111, 147, 168}, {112, 148, 169}, {114, 149, 170}, {115, 150, 171}, {116, 151, 172}, {117, 151, 172}, {118, 152, 173}, {119, 153, 174}, {120, 154, 175}, {121, 155, 176}, {122, 156, 176}, {123, 157, 177}, {124, 158, 178}, {125, 159, 179}, {126, 160, 179}, {127, 160, 180}, {128, 161, 181}, {129, 162, 181}, {130, 163, 182}, {131, 164, 183}, {132, 164, 183}, {133, 165, 184}, {134, 166, 185}, {135, 167, 185}, {136, 168, 186}, {137, 168, 187}, {138, 169, 187}, {139, 170, 188}, {140, 171, 189}, {141, 171, 189}, {141, 172, 190}, {142, 173, 190}, {143, 173, 191}, {144, 174, 192}, {145, 175, 192}, {146, 176, 193}, {147, 176, 193}, {148, 177, 194}, {148, 178, 194}, {149, 178, 195}, {150, 179, 195}, {151, 180, 196}, {152, 180, 197}, {153, 181, 197}, {153, 182, 198}, {154, 182, 198}, {155, 183, 199}, {156, 184, 199}, {157, 184, 200}, {158, 185, 200}, {158, 186, 201}, {159, 186, 201}, {160, 187, 202}, {161, 187, 202}, {162, 188, 203}, {162, 189, 203}, {163, 189, 204}, {164, 190, 204}, {165, 190, 205}, {165, 191, 205}, {166, 192, 206}, {167, 192, 206}, {168, 193, 207}, {168, 193, 207}, {169, 194, 208}, {170, 194, 208}, {171, 195, 208}, {171, 196, 209}, {172, 196, 209}, {173, 197, 210}, {174, 197, 210}, {174, 198, 211}, {175, 198, 211}, {176, 199, 212}, {177, 199, 212}, {177, 200, 212}, {178, 201, 213}, {179, 201, 213}, {179, 202, 214}, {180, 202, 214}, {181, 203, 215}, {182, 203, 215}, {182, 204, 215}, {183, 204, 216}, {184, 205, 216}, {184, 205, 217}, {185, 206, 217}, {186, 206, 217}, {186, 207, 218}, {187, 207, 218}, {188, 208, 219}, {188, 208, 219}, {189, 209, 219}, {190, 209, 220}, {190, 210, 220}, {191, 210, 221}, {192, 211, 221}, {192, 211, 221}, {193, 212, 222}, {194, 212, 222}, {194, 213, 222}, {195, 213, 223}, {196, 214, 223}, {196, 214, 224}, {197, 215, 224}, {198, 215, 224}, {198, 216, 225}, {199, 216, 225}, {200, 216, 225}, {200, 217, 226}, {201, 217, 226}, {201, 218, 226}, {202, 218, 227}, {203, 219, 227}, {203, 219, 228}, {204, 220, 228}, {205, 220, 228}, {205, 221, 229}, {206, 221, 229}, {206, 221, 229}, {207, 222, 230}, {208, 222, 230}, {208, 223, 230}, {209, 223, 231}, {210, 224, 231}, {210, 224, 231}, {211, 224, 232}, {211, 225, 232}, {212, 225, 232}, {213, 226, 233}, {213, 226, 233}, {214, 227, 233}, {214, 227, 234}, {215, 227, 234}, {216, 228, 234}, {216, 228, 235}, {217, 229, 235}, {217, 229, 235}, {218, 229, 235}, {218, 230, 236}, {219, 230, 236}, {220, 231, 236}, {220, 231, 237}, {221, 231, 237}, {221, 232, 237}, {222, 232, 238}, {222, 233, 238}, {223, 233, 238}, {224, 233, 239}, {224, 234, 239}, {225, 234, 239}, {225, 235, 239}, {226, 235, 240}, {226, 235, 240}, {227, 236, 240}, {228, 236, 241}, {228, 237, 241}, {229, 237, 241}, {229, 237, 242}, {230, 238, 242}, {230, 238, 242}, {231, 239, 242}, {231, 239, 243}, {232, 239, 243}, {233, 240, 243}, {233, 240, 244}, {234, 240, 244}, {234, 241, 244}, {235, 241, 244}, {235, 242, 245}, {236, 242, 245}, {236, 242, 245}, {237, 243, 246}, {237, 243, 246}, {238, 243, 246}, {238, 244, 246}, {239, 244, 247}, {240, 244, 247}, {240, 245, 247}, {241, 245, 247}, {241, 246, 248}, {242, 246, 248}, {242, 246, 248}, {243, 247, 249}, {243, 247, 249}, {244, 247, 249}, {244, 248, 249}, {245, 248, 250}, {245, 248, 250}, {246, 249, 250}, {246, 249, 250}, {247, 249, 251}, {247, 250, 251}, {248, 250, 251}, {248, 250, 251}, {249, 251, 252}, {249, 251, 252}, {250, 251, 252}, {250, 252, 252}, {251, 252, 253}, {251, 252, 253}, {252, 253, 253}, {252, 253, 253}, {253, 253, 254}, {253, 254, 254}, {254, 254, 254}, {255, 255, 255}};