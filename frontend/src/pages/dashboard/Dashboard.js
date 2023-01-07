import React, { useState, useEffect } from "react";
import Card from "../../components/card/Card";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
import axios from "axios";

export default function Dashboard() {
  const [jobss, setMyJobs] = useState([]);
  useEffect(() => {
    axios.get("http://localhost:90/jobs").then((res) => {
      console.log(res);
      setMyJobs(res.data);
    });
  }, []);

  const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
  };
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  const [job, setJob] = useState({
    name: "",
    desc: "",
    skills: "",
    edu: "",
    exp: "",
  });
  const [jobs, setJobs] = useState([]);
  const handleInput = (e) => {
    const name = e.target.name;
    const value = e.target.value;
    console.log(name, value);
    setJob({ ...job, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newJob = {
      ...job,
      id: new Date().getTime().toString(),
    };
    setJobs([...jobs, job]);
    console.log(jobs);
  };

  return (
    <div className="dashboard">
      <Modal
        hideBackdrop
        open={open}
        onClose={handleClose}
        aria-labelledby="child-modal-title"
        aria-describedby="child-modal-description"
      >
        <Box className="box" sx={{ width: 200, ...style }}>
          <form onSubmit={handleSubmit}>
            <div>
              <label htmlform="name">Name</label>
              <input
                onChange={handleInput}
                type="text"
                value={job.name}
                name="name"
                id="name"
              />
            </div>
            <div>
              <label htmlform="desc">Description</label>
              <input
                onChange={handleInput}
                type="text"
                value={job.desc}
                name="desc"
                id="desc"
              />
            </div>
            <div>
              <label htmlform="skills">Skills</label>
              <input
                onChange={handleInput}
                type="text"
                value={job.skills}
                name="skills"
                id="skills"
              />
            </div>
            <div>
              <label htmlform="edu">Education</label>
              <input
                onChange={handleInput}
                type="text"
                value={job.edu}
                name="edu"
                id="edu"
              />
            </div>
            <div>
              <label htmlform="exp">Experience</label>
              <input
                onChange={handleInput}
                type="text"
                value={job.exp}
                name="exp"
                id="exp"
              />
            </div>
            <button type="submit">Submit</button>
          </form>
        </Box>
      </Modal>
      <div className="create-job btn btn-outline-success" onClick={handleOpen}>
        Create
      </div>
      <div className="grid">
        {jobss.map((post) => {
          const { name, desc, skills, edu, exp } = post
          return <Card cardTitle={name} cardText={skills + '\n'+ edu}  />;
        })}
      </div>
    </div>
  );
}
