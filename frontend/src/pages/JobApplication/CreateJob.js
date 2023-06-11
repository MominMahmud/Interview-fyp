import React, { useState, useEffect } from "react";
import Card from "../../components/card/Card";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import axios from "axios";
import requests from '../../config'
export default function CreateJob() {

  var [questions, setQuestions] = useState([]);
  const [state,setState] = useState(0);
  useEffect(() => {
    if(state==0){
      setState(1);
      axios.get(requests.getQuestions).
      then((res) => {
        const quest = [];
        console.log('Response:',res.data);
        for(let i =0;i<res.data.length;i++){
          quest.push(res.data[i].text)
        }
        setQuestions(quest);
      });
    }
  },[])
  const [job, setJob] = useState({
    name: "",
    desc: "",
    skills: "",
    edu: "",
    exp: "",
    
  });
  const [jobs, setJobs] = useState([]);
  const [invalid,setInvalid]=useState("")
  const handleInput = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    console.log(name, value);
    setJob({ ...job, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault()
    const newJob = {
      ...job,
      id: new Date().getTime().toString(),
    };
    setJobs([...jobs, job]);
    axios.post(requests.createJobs, {
      name: job.name,
      desc: job.desc,
      skills: job.skills,
      edu: job.edu,
      exp: job.exp,
      questions:selectedQuestions
    });
    console.log(selectedQuestions);
  };

  const [showJobForm, setShowJobForm] = useState(true);
  function setQuestionsToTrue(e) {
    e.preventDefault();
    
    if(job.name && job.desc && job.skills && job.edu && job.exp){
      setShowJobForm(false);
      setInvalid("")
    }
    else{

      setInvalid("Please fill all the fields")
    }
    console.log(showJobForm);
  }


  const [selectedQuestions, setSelectedQuestions] = useState([]);

  return (
    <div>
      <Box className="box-box mt-4">
        <div className="create-job">
          <form className={showJobForm ? "" : "hideJobForm"}>
            <div className="row">
              <div className="my-1">
                <label htmlform="name">Name</label>
                <input
                  className="col-12"
                  onChange={handleInput}
                  type="text"
                  value={job.name}
                  name="name"
                  id="name"
                />
              </div>
              <div className="my-1">
                <label htmlform="desc">Description</label>
                <textarea
                  className="col-12"
                  onChange={handleInput}
                  type="text"
                  value={job.desc}
                  name="desc"
                  id="desc"
                />
              </div>
              <div className="my-1">
                <label htmlform="skills">Skills</label>
                <input
                  className="col-12"
                  onChange={handleInput}
                  type="text"
                  value={job.skills}
                  name="skills"
                  id="skills"
                />
              </div>
              <div className="my-1">
                <label htmlform="edu">Education</label>
                <input
                  className="col-12"
                  onChange={handleInput}
                  type="text"
                  value={job.edu}
                  name="edu"
                  id="edu"
                />
              </div>
              <div className="my-1">
                <label htmlform="exp">Experience</label>
                <input
                  className="col-12"
                  onChange={handleInput}
                  type="text"
                  value={job.exp}
                  name="exp"
                  id="exp"
                />
              </div>
            </div>

            <div className="my-3 d-flex justify-content-between">
            <div className="text-danger">
              {invalid}
            </div>
              <button className="btn btn-primary " onClick={setQuestionsToTrue}>
                Next
              </button>
            </div>
          </form>

          <form className={showJobForm ? "hideJobForm" : ""}>
          <h4>Select Questions</h4>
            <div>

              
              {questions.map((item) => (
                <label key={item} className="mb-3">
                  <input
                    className="mx-3"
                    type="checkbox"
                    value={item}
                    checked={selectedQuestions.includes(item)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedQuestions([...selectedQuestions, item]);
                      } else {
                        setSelectedQuestions(
                          selectedQuestions.filter((i) => i !== item)
                        );
                      }
                    }}
                  />
                  <span>{item}</span>
                </label>
              ))}
            </div>
            <button className="btn btn-primary" onClick={handleSubmit}>Submit</button>
          </form>
        </div>
      </Box>
    </div>
  );
}
