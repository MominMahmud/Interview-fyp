import React from "react";
import Card from "../../components/card/Card";
import { useState, useEffect } from "react";
import axios from 'axios'
import requests from '../../config'

export default function Dashboard() {
  const [jobss, setMyJobs] = useState([]);
  const [searchVal, setSearchVal] = useState("");
  const [filteredJobs, setFilteredJobs] = useState([])
  function handleSearchClick() {
    console.log(searchVal)
    if (searchVal === "") { setFilteredJobs(jobss); return; }
    const filterBySearch = jobss.filter((item) => {
      if (item.name.toLowerCase()
        .includes(searchVal.toLowerCase())) { return item; }
    })
    setFilteredJobs(filterBySearch);
  }
  function handleResetClick() {

    setFilteredJobs(jobss)
  }
  useEffect(()=>{
    handleSearchClick()

  },[searchVal])
  useEffect(() => {
    axios.get(requests.getJobs).then((res) => {
      console.log(res);
      setMyJobs(res.data.reverse());
      setFilteredJobs(res.data.reverse().reverse())
    });
  }, []);
  const handleClick = () => {
    window.open("/create/job");

  }

  return (
    <div className="dashboard">
      <div class="row justify-content-between">
        <div class="col-6 d-flex">
          <input className="form-control" placeholder="Search.." value={searchVal} onChange={(e) => {
            setSearchVal(e.target.value)
            
          }}></input>
          <button className="mx-3 btn btn-success" onClick={handleSearchClick}>Go</button>
          <button className="btn btn-outline-primary" onClick={handleResetClick}>Reset</button>
        </div>
        <div class="col-3 " >
          <button className="btn btn-outline-success" onClick={handleClick}>Create</button>
        </div>
      </div>
      <div className="row">
        {filteredJobs.map((post) => {
          const { _id, name, desc, skills, edu, exp } = post;
          return (
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{name}</h5>
                <p class="card-text">
                  <b>Education</b>: {edu}
                </p>
                <p class="card-text">
                  <b>Skills:</b> {skills}
                </p>
                <p className="card-text">
                  <b>Experience:</b> {exp}
                </p>
                <a
                  className="btn btn-primary btn-sm"
                  href={"/candidates/?id=" + _id}
                >
                  View Candidates
                </a>
              </div>

            </div>

          )
        })}
      </div>
    </div>)
}

