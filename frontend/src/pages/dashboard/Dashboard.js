import React from "react";
import Card from "../../components/card/Card";
import { useState, useEffect } from "react";
import axios from 'axios'
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

  const handleClick = () => {
    window.open("/create/job");

  }

  return (
    <div className="dashboard">
      <button className="btn btn-outline-success" onClick={handleClick}>Create</button>
      <div className="grid">
        {jobss.map((post) => {
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

