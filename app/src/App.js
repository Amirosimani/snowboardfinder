import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import jsonData from './info-json';
import List2 from './List2';

class App extends Component {

  constructor(){
    super();

    this.state={
      search: null,
      items: jsonData.reduce((a, v) => ({ ...a, [v['id']]: v}), {}),
      results: jsonData.map(i => i.id),
      selectedItems: []
    };
  }

  setSelected = (e) => {
    this.setState({
      ...this.state,
      selectedItems: [1]
    });
    
  }
  
  searchSpace=(event) => {
    let keyword = event.target.value;
    let results = [];
    if(keyword === null) {
      results = this.state.items.map(i => i.id);
    } else {
      results =  Object.entries(this.state.items).map(([id, item]) => item).filter(
        i => i.meta_data.name.toLowerCase().includes(keyword.toLowerCase()));      
    }

    // console.log(this.state.results);
    
    this.setState({
      ...this.state,
      results: results.map(i => i.id),
      search: keyword
    })
  }

  render(){
    const styleInfo = {
      paddingRight:'10px',
      textDecoration: 'none',
      color: '#000000'
    }
    const elementStyle ={
      border:'solid',
      borderRadius:'10px',
      position:'relative',
      left:'10vh',
      height:'3vh',
      width:'20vh',
      marginTop:'5vh',
      marginBottom:'10vh'

    }
    let items = this.state.results.map(id => {
      let item = this.state.items[id];
      return(
      <div>
        <ul>
          <li style={{position:'relative', left:'10vh'}}>
            <a onClick={(e)=>this.setSelected(e)} style={styleInfo} href={item.meta_data.url} target="_blank"><span style={styleInfo} >{item.meta_data.name.replace('-snowboard-review','').replace('-snowboard-reveiw','')}</span></a>
          </li>
        </ul>
      </div>
      )
    })
    return (
      <div>
        <input type="text" placeholder="Enter item to be searched" style={elementStyle} onChange={(e)=>this.searchSpace(e)} />
        <div id="container">
          <div id="left-container">
          {items}
          </div>
        <div id="right-container">
          <List2 selectedItems={this.state.selectedItems}></List2>
        </div>
        
      </div>
      
      </div>
    )
  }

}

export default App;