import React from 'react'
import Profile from './profile/Profile'
import Navbar from './side-nav/Navbar'
import Header from './header/Header'
export default function Components(props) {
  return (
    <div>
        <Profile/>
        <Navbar/>
        <Header head={props.header}/>
    </div>
  )
}
