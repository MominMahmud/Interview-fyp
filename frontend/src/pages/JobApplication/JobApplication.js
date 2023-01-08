import React, { useState, useEffect } from "react";
import axios from "axios";

export default function JobApplication() {
  const [jobs, setMyJobs] = useState([]);
  useEffect(() => {
    axios.get("http://localhost:90/jobs").then((res) => {
      console.log(res);
      setMyJobs(res.data);
    });
  }, []);
  const [candidate, setCandidate] = useState({
    name: "",
    email:"",
    age: "",
    experience: "",
    status: "0",
    ranking: "0",
    score: "0",
    appliedfor: "",
  });
  const handleInput = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    console.log(name, value);
    setCandidate({ ...candidate, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("http://localhost:90/candidates", {
      name: candidate.name,
      email:candidate.email,
      age: candidate.age,
      experience: candidate.experience,
      status: candidate.status,
      ranking: candidate.ranking,
      score: candidate.score,
      appliedfor: candidate.appliedfor,
    });
    console.log(candidate);
  };
  return (
    <>
      <div className="answer"></div>
      <div id="background"></div>
      <div className="interview-section">
        <form onSubmit={handleSubmit}>
          <h3>Job Application</h3>
          <div className="row w-50 mx-auto">
            <div>
              <label htmlform="name">Name</label>
              <input
                className="col-12"
                onChange={handleInput}
                type="text"
                value={candidate.name}
                name="name"
                id="name"
              />
            </div>
            <div>
              <label htmlform="email">Email</label>
              <input
                className="col-12"
                onChange={handleInput}
                type="email"
                value={candidate.email}
                name="email"
                id="email"
              />
            </div>
            <div>
              <label htmlform="age">Age</label>
              <input
                className="col-12"
                onChange={handleInput}
                type="text"
                value={candidate.age}
                name="age"
                id="age"
              />
            </div>
            <div>
              <label htmlform="experience">Experience</label>
              <input
                className="col-12"
                onChange={handleInput}
                type="text"
                value={candidate.experience}
                name="experience"
                id="experience"
              />
            </div>
            <div>
              <label htmlform="appliedfor">Select a Job</label>
              <select
                class="form-select col-12"
                aria-label=".form-select-lg example"
                name="appliedfor"
                id="appliedfor"
                onChange={handleInput}
              >
                {jobs.map((post)=>{
                    const {_id,name,desc,skills,edu,exp } = post
                    return <option className="drop-down">{name}</option>
                })}
              </select>
            </div>

            <button type="submit" className="btn btn-primary w-25 mt-4">
              Apply
            </button>
          </div>
        </form>
      </div>
    </>
  );
}
