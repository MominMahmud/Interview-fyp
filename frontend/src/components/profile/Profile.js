import React from 'react'
import profile from '../../images/profilee.png'
export default function Profile() {
  return (
    <div>
      <div className='profileBackground'></div>
      <div id='profileInfo'>
        <img src={profile} alt='Picture' className='profilePicture'></img>
        <div className='profileText'>Waleed Mukhtar</div>
      </div>
    </div>
  )
}
