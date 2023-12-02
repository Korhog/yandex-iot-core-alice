struct RGB {
  unsigned char r;
  unsigned char g;
  unsigned char b;
  
  static RGB FromRGB(unsigned char r, unsigned char g, unsigned char b) {
    RGB res;
    res.r = r;
    res.g = g;
    res.b = b;

    return res;
  }

    static RGB Black() {
    RGB res;
    res.r = 0;
    res.g = 0;
    res.b = 0;

    return res;
  }
};

unsigned char Clamp(unsigned char value, unsigned char min, unsigned char max) {
    if (value < min) return min;
    if (value > max) return max;

    return value;
};

RGB Mix(RGB from, RGB to, unsigned char step, unsigned char size = 255) {
    RGB result;
    result.r = Clamp(from.r + step * ((float)(to.r - from.r)/(float)size), 0, 255);
    result.g = Clamp(from.g + step * ((float)(to.g - from.g)/(float)size), 0, 255);
    result.b = Clamp(from.b + step * ((float)(to.b - from.b)/(float)size), 0, 255);

    return result;
};




