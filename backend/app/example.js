const circle = {
  radius: 10,
  color: "orange",
  getArea: function () {
    return circle.radius * circle.radius * Math.PI;
  },
  getCircumference: function () {
    return 2 * Math.PI * this.radius;
  },
};

let { radius, getArea, getCircumference } = circle;
//i need the circles area applying structuring to find the area with the radius given
console.log(getArea.call(circle)); //not like this

//this is how you do it
console.log(circle.getArea());
