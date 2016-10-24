import graph;
size(400);
pen p=rgb(0, 0, 1);

real x1(real t){
  return cos(t) + 0.65 * cos(2 * t) - 0.65;
}
real x2(real t){
  return 1.5 * sin(t);
}

draw(graph(x1, x2, 0, 2*pi), p);
