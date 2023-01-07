import React from "react";
import Card from "../../components/card/Card";
import Box from "@mui/material/Box";
import Modal from "@mui/material/Modal";
export default function Dashboard() {
  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  }
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
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
          <form>
            <div class="form-group">
              <label for="exampleInputEmail1">Email address</label>
              <input
                type="email"
                class="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                placeholder="Enter email"
              />
              <small id="emailHelp" class="form-text text-muted">
                We'll never share your email with anyone else.
              </small>
            </div>
            <div class="form-group">
              <label for="exampleInputPassword1">Password</label>
              <input
                type="password"
                class="form-control"
                id="exampleInputPassword1"
                placeholder="Password"
              />
            </div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="exampleCheck1"
              />
              <label class="form-check-label" for="exampleCheck1">
                Check me out
              </label>
            </div>
            <button type="submit" class="btn btn-primary">
              Submit
            </button>
            <button className='btn btn-primary'onClick={handleClose}>Close</button>

          </form>
        </Box>
      </Modal>
      <div className="create-job btn btn-outline-success" onClick={handleOpen}>
        Create
      </div>
      <div className="row">
        <div className="col">
          <Card
            cardTitle="Software Engineer"
            cardText="Bot interviewing for hiring Software Enginners"
            value="75"
          />
        </div>
        <div className="col">
          <Card
            cardTitle="Web Developer"
            cardText="Bot interviewing for hiring Web Developers"
            value="10"
          />
        </div>
        <div className="col">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">ML Enginner</h5>
              <p className="card-text">
                Bot interviewing for hiring ML Enginners
              </p>
              <div class="progress">
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  aria-valuenow="75"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
              <a href="#" class="btn btn-primary">
                View Candidates
              </a>
            </div>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Software Engineer</h5>
              <p className="card-text">
                Bot interviewing for hiring Software Enginners
              </p>
              <div class="progress">
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  aria-valuenow="75"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
              <a href="#" class="btn btn-primary">
                View Candidates
              </a>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Web Developer</h5>
              <p className="card-text">
                Bot interviewing for hiring Web Developerss
              </p>
              <div class="progress">
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  aria-valuenow="75"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
              <a href="#" class="btn btn-primary">
                View Candidates
              </a>
            </div>
          </div>
        </div>
        <div className="col">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">ML Enginner</h5>
              <p className="card-text">
                Bot interviewing for hiring ML Enginners
              </p>
              <div class="progress">
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  aria-valuenow="75"
                  aria-valuemin="0"
                  aria-valuemax="100"
                ></div>
              </div>
              <a href="#" class="btn btn-primary">
                View Candidates
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
