Ring = bytearray([
	0b00000111, 0b11100000,
	0b00011000, 0b00011000,
	0b00100001, 0b10000100,
	0b01000110, 0b01100010,
	0b01001000, 0b00010010,
	0b10010001, 0b10001001,
	0b10010010, 0b01001001,
	0b10100100, 0b00100101,
	0b10100100, 0b00100101,
	0b10010010, 0b01001001,
	0b10010001, 0b10001001,
	0b01001000, 0b00010010,
	0b01000110, 0b01100010,
	0b00100001, 0b10000100,
	0b00011000, 0b00011000,
	0b00000111, 0b11100000])

PlayerIcon = bytearray([
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000001, 0b00000000,
	0b00000011, 0b10000000,
	0b00000011, 0b10000000,
	0b01111111, 0b11111100,
	0b11111111, 0b11111110,
	0b11111111, 0b11111110,
	0b11111111, 0b11111110,
	0b11111111, 0b11111110])

PlayerP1 = bytearray([
	0b00000000, 0b00000011,
	0b00000000, 0b00000011,
	0b00000000, 0b00001111,
	0b00000000, 0b00001111,
	0b00000000, 0b00001111,
	0b00000000, 0b00001111,
	0b00111111, 0b11111111,
	0b00111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111])

PlayerP2 = bytearray([
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b11000000, 0b00000000,
	0b11000000, 0b00000000,
	0b11000000, 0b00000000,
	0b11000000, 0b00000000,
	0b11111111, 0b11110000,
	0b11111111, 0b11110000,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100,
	0b11111111, 0b11111100])

Player = bytearray([
	0b00000000, 0b00001100, 0b00000000, 0b00000000,
	0b00000000, 0b00001100, 0b00000000, 0b00000000,
	0b00000000, 0b00111111, 0b00000000, 0b00000000,
	0b00000000, 0b00111111, 0b00000000, 0b00000000,
	0b00000000, 0b00111111, 0b00000000, 0b00000000,
	0b00000000, 0b00111111, 0b00000000, 0b00000000,
	0b00111111, 0b11111111, 0b11111111, 0b00000000,
	0b00111111, 0b11111111, 0b11111111, 0b00000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,
	0b11111111, 0b11111111, 0b11111111, 0b11000000,])

Blank = bytearray([
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000,
	0b00000000, 0b00000000])

Cursor = bytearray([
	0b00000000, 0b00000000,
	0b00111111, 0b11111100,
	0b01111111, 0b11111110,
	0b01111111, 0b11111110,
	0b01111000, 0b00011110,
	0b01110000, 0b00001110,
	0b01110000, 0b00001110,
	0b01110000, 0b00001110,
	0b01110000, 0b00001110,
	0b01110000, 0b00001110,
	0b01110000, 0b00001110,
	0b01111000, 0b00011110,
	0b01111111, 0b11111110,
	0b01111111, 0b11111110,
	0b00111111, 0b11111100,
	0b00000000, 0b00000000])

Alien1 = bytearray([
	0b00000011, 0b11000000,
	0b00000011, 0b11000000,
	0b00001111, 0b11110000,
	0b00001111, 0b11110000,
	0b00111111, 0b11111100,
	0b00111111, 0b11111100,
	0b11110011, 0b11001111,
	0b11110011, 0b11001111,
	0b11111111, 0b11111111,
	0b11111111, 0b11111111,
	0b00001100, 0b00110000,
	0b00001100, 0b00110000,
	0b00110011, 0b11001100,
	0b00110011, 0b11001100,
	0b11001100, 0b00110011,
	0b11001100, 0b00110011])

Alien2 = bytearray([
	0b00001100, 0b00000000, 0b11000000, 0b00000000,
	0b00001100, 0b00000000, 0b11000000, 0b00000000,
	0b00000011, 0b00000011, 0b00000000, 0b00000000,
	0b00000011, 0b00000011, 0b00000000, 0b00000000,
	0b00001111, 0b11111111, 0b11000000, 0b00000000,
	0b00001111, 0b11111111, 0b11000000, 0b00000000,
	0b00111100, 0b11111100, 0b11110000, 0b00000000,
	0b00111100, 0b11111100, 0b11110000, 0b00000000,
	0b11111111, 0b11111111, 0b11111100, 0b00000000,
	0b11111111, 0b11111111, 0b11111100, 0b00000000,
	0b11001111, 0b11111111, 0b11001100, 0b00000000,
	0b11001111, 0b11111111, 0b11001100, 0b00000000,
	0b11001100, 0b00000000, 0b11001100, 0b00000000,
	0b11001100, 0b00000000, 0b11001100, 0b00000000,
	0b00000011, 0b11001111, 0b00000000, 0b00000000,
	0b00000011, 0b11001111, 0b00000000, 0b00000000,])

Alien3 = bytearray([
	0b00000000, 0b11111111, 0b00000000, 0b00000000,
	0b00000000, 0b11111111, 0b00000000, 0b00000000,
	0b00111111, 0b11111111, 0b11111100, 0b00000000,
	0b00111111, 0b11111111, 0b11111100, 0b00000000,
	0b11111111, 0b11111111, 0b11111111, 0b00000000,
	0b11111111, 0b11111111, 0b11111111, 0b00000000,
	0b11111100, 0b00111100, 0b00111111, 0b00000000,
	0b11111100, 0b00111100, 0b00111111, 0b00000000,
	0b11111111, 0b11111111, 0b11111111, 0b00000000,
	0b11111111, 0b11111111, 0b11111111, 0b00000000,
	0b00001111, 0b11000011, 0b11110000, 0b00000000,
	0b00001111, 0b11000011, 0b11110000, 0b00000000,
	0b00111100, 0b00111100, 0b00111100, 0b00000000,
	0b00111100, 0b00111100, 0b00111100, 0b00000000,
	0b00001111, 0b00000000, 0b11110000, 0b00000000,
	0b00001111, 0b00000000, 0b11110000, 0b00000000,])