import React, { useState, useEffect } from "react";
import axios from "axios";
import requests from '../../config'

export default function JobApplication() {
  const [jobs, setMyJobs] = useState([]);
  const [invalid, setInvalid] = useState("")
  useEffect(() => {
    axios.get(requests.getJobs).then((res) => {
      console.log(res);
      setMyJobs(res.data);
    });
  }, []);
  const [candidate, setCandidate] = useState({

    name: "",
    email: "",
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
    if (candidate.name && candidate.email && candidate.age && candidate.experience &&
      candidate.experience && candidate.appliedfor) {

      setInvalid("")

      axios
        .post(requests.createCandidate, {
          name: candidate.name,
          email: candidate.email,
          age: candidate.age,
          experience: candidate.experience,
          status: candidate.status,
          ranking: candidate.ranking,
          score: candidate.score,
          appliedfor: candidate.appliedfor,

        })
        .then(
          () => {
            axios.get(requests.getCandidateEmail + '/' + candidate.email).then((res) => {
              console.log(res);
            })
          }
        );
      console.log(candidate);
    }
    else {
      setInvalid("Please fill all the details..")
      e.preventDefault()
    }
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
                {jobs.map((post) => {
                  const { _id, name, desc, skills, edu, exp } = post;
                  return <option className="drop-down">{name}</option>;
                })}
              </select>
            </div>

            <div className='d-flex justify-content-between align-items-center'>
              <button type="submit" className="btn btn-primary w-25 mt-4">
                Apply
              </button>
              <div className="text-danger">
                {invalid}
              </div>
            </div>
          </div>
        </form>
      </div>
    </>
  );
}