import React from "react";
import Card from "../../components/card/Card";
export default function Dashboard() {
  return (
    <div className="dashboard">
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
