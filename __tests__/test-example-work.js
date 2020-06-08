import React from 'react';
import { shallow } from 'enzyme';
import ExampleWork, { ExampleWorkBubble } from '../js/example-work';

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
Enzyme.configure({ adapter: new Adapter() });

const myWork = [
  {
  'title': "Work Example",
  'image':{
    'desc':"example screenshot of a project involving code",
    'src':"images/example1.png",
    'comment':""
  }
},
{
'title': "Portfolio Boilerplate",
'image':{
  'desc':"A serverless Portfolio",
  'src':"images/example2.png",
  'comment':`“Chemistry” by Surian Soosay is licensed under CC BY 2.0
  https://www.flickr.com/photos/ssoosay/4097410999`
}
},
{
'title': "Work Example",
'image':{
  'desc':"example screenshot of a project involving cats",
  'src':"images/example3.png",
  'comment':`“Bengal cat” by roberto shabs is licensed under CC BY 2.0
                 https://www.flickr.com/photos/37287295@N00/2540855181`
}
}

]

// test ExampleWork Component
describe("ExampleWork component", ()=>{
  let component = shallow(<ExampleWork work={myWork}/>);

  it("Should be a section element", ()=>{
    // console.log(component.debug()); // this line helps you see what shallow picks up above
    expect(component.type()).toEqual('section');
  });

  it("Should contain as many Children as there are work examples ",  ()=>{
    expect(component.find("ExampleWorkBubble").length).toEqual(myWork.length);
  });

});

// test ExampleWorkBubble component

describe("ExampleWorkBubble component", ()=>{
  let component = shallow(<ExampleWorkBubble example={myWork[1]}/>);
  let images = component.find("img");

  it("should contain a single image 'img' element", ()=>{
    expect(images.length).toEqual(1);
  });

  it("should have the image source set correctly", ()=>{
    expect(images.prop('src')).toEqual(myWork[1].image.src);
  });
});
