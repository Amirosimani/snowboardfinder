import React, { Component } from 'react';
// import logo from './logo.svg';
import './List2.css';

class List2 extends Component {

  constructor(){
    super();
    this.state= {
      similarities: [],
    };
  }

  render(){
  console.log(...this.props.selectedItems)
    return (
      <div> Suck it</div>
    )
  }

}


export default List2;