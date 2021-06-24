import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import getData from './info-json';


class App extends Component {

  constructor(){
    super();

    this.state={
      search:null
    };
  }

  searchSpace=(event)=>{
    let keyword = event.target.value;
    this.setState({search:keyword})
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
    const items = getData.filter((data)=>{
      if(this.state.search == null)
          return data
      else if(data.meta_data.name.toLowerCase().includes(this.state.search.toLowerCase())){
          return data
      }
    }).map(data=>{
      return(
      <div>
        <ul>
          <li style={{position:'relative',left:'10vh'}}>
            <a style={styleInfo} href={data.meta_data.url} target="_blank"><span style={styleInfo} >{data.meta_data.name.replace('-snowboard-review','').replace('-snowboard-reveiw','')}</span></a>
          </li>
        </ul>
      </div>
      )
    })

    return (
      <div>
      <input type="text" placeholder="Enter item to be searched" style={elementStyle} onChange={(e)=>this.searchSpace(e)} />
      {items}
      </div>
    )
  }
}

export default App;